import json
import logging
from typing import List
from uuid import UUID

from cachetools import TTLCache, cached
from pydantic import BaseSettings

from .base import BasePersistenceManager
from .echarts_util import echarts_option_translation_update
from .model.chart_models import DataSourceSeriesDO, FieldMappingDO, DataSourceType, FilterDO
from .model.dashboard_models import DashboardDO, FieldValue
from ..persistence.cubejs_client import CubejsClient

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class VisualizationDomainHandler(BaseSettings):
    persistence_manager: BasePersistenceManager
    cubejs_client: CubejsClient

    def hash_key_dashboard(self, tenant_id: UUID, tenant_code: str, dashboard_id: UUID, filter_list: List[FilterDO]):
        return (
            tenant_id,
            dashboard_id,
            tuple(filter_list)
        )

    def hash_key_dashboards(self, tenant_id: UUID, tenant_code: str, frontend_key: str, include_components: bool):
        return tenant_id, frontend_key, include_components

    @cached(cache=TTLCache(maxsize=32, ttl=300), key=hash_key_dashboard)
    def get_dashboard(self, tenant_id: UUID, tenant_code: str, dashboard_id: UUID, filter_list: List[FilterDO]):
        dashboard = self.persistence_manager.get_dashboard(tenant_id, dashboard_id)
        return self._get_dashboard_info(tenant_id, tenant_code, dashboard, filter_list, include_components=True)

    @cached(cache=TTLCache(maxsize=32, ttl=300), key=hash_key_dashboards)
    def get_dashboards(self, tenant_id: UUID, tenant_code: str, frontend_key: str, include_components: bool):
        dashboards = self.persistence_manager.get_dashboards(tenant_id, frontend_key)
        return [
            self._get_dashboard_info(tenant_id, tenant_code, dashboard, [], include_components)
            for dashboard in dashboards
        ]

    @staticmethod
    def get_view_field_name(db_field):
        if db_field == 'categories':
            return 'Categories.category'
        elif db_field == 'taxonomyTags':
            return 'TaxonomyTags.taxonomyTag'
        elif db_field == 'taxonomyTerms':
            return 'TaxonomyTerms.taxonomyTerm'
        else:
            return 'ProcessedDataViewV1.' + db_field

    def _get_dashboard_info(self, tenant_id: UUID, tenant_code: str, dashboard: DashboardDO,
                            filter_list: List[FilterDO], include_components: bool):
        if not include_components:
            dashboard.component_layout = None
            return dashboard

        dashboard.component_layout.components = [component
                                                 for component in dashboard.component_layout.components
                                                 if not component.disabled]

        chart_ids = [component.identifier
                     for component in dashboard.component_layout.components
                     if component.identifier is not None]
        charts = self.persistence_manager.get_charts_by_ids(tenant_id, chart_ids)

        filter_map = {filter_obj.name: filter_obj for filter_obj in filter_list}
        self.cubejs_client.update_cubejs_fields(filter_list)
        for component in dashboard.component_layout.components:
            if component.type == 'chart':
                chart = charts[component.identifier]
                component.inputs.append(FieldValue(
                    field='chart_config',
                    value={'chart_type': chart.chart_type, 'option': chart.chart_config}
                ))
                series_data = self.get_series_data(tenant_code,
                                                   chart.data_source_type,
                                                   chart.data_source_series,
                                                   chart.data_field_mapping,
                                                   filter_list)
                if chart.chart_type == 'echarts':
                    echarts_option_translation_update(chart.chart_config, series_data)
            elif component.type == 'react-component':
                if component.name == 'FilterPanel':
                    for input_obj in component.inputs:
                        if input_obj.field == "filters":
                            for filter_value in input_obj.value:
                                if 'db_field' in filter_value:
                                    db_field = filter_value.pop('db_field')
                                    filter_field = filter_value.get('id')
                                    if db_field:
                                        field_name = self.get_view_field_name(db_field)
                                        query = {"dimensions": [field_name]}
                                        result = self.cubejs_client.fetch_data(tenant_code, query, [])
                                        result_values = [{"code": dp[field_name]} for dp in result
                                                         if len(dp[field_name].strip()) > 0]
                                        filter_value['options'] = [{"code": "all"}]
                                        filter_value['options'].extend(result_values)

                                        if filter_field in filter_map:
                                            filter_value['selectedValue'] = {'code': filter_map[filter_field].values[0]}
                                        else:
                                            filter_value['selectedValue'] = filter_value['defaultValue']
                elif component.name == 'LiveFeedTable':
                    query_obj = None
                    for input_obj in component.inputs:
                        if input_obj.field == "query":
                            query_obj = input_obj
                    if query_obj:
                        query = query_obj.value
                        component.inputs.remove(query_obj)
                        result = self.cubejs_client.fetch_data(tenant_code, query, filter_list)
                        component.inputs.append(FieldValue(
                            field="live_feeds",
                            value=[{key.replace('ProcessedDataViewV1.', ''): value
                                    for key, value in entry.items()}
                                   for entry in result]
                        ))

        return dashboard

    def get_series_data(self, tenant_code: str,
                        data_source_type: DataSourceType,
                        data_source_series: List[DataSourceSeriesDO],
                        field_mapping_list: List[FieldMappingDO],
                        filter_list: List[FilterDO]) -> List[List[dict]]:

        # create name mapping map: { 'common': { 'x': 'p.abc'}, 'series1': { 'y': 'abc' } }
        # series mapping will override common mappings
        field_mappings = {'common': {}}
        for field_mapping in field_mapping_list:
            series = field_mapping.series if field_mapping.series else 'common'
            if series not in field_mappings:
                field_mappings[series] = {}
            field_mappings[series][field_mapping.data_field] = field_mapping.chart_field

        result_series = []
        if data_source_type == DataSourceType.CUBE_JS:
            for data_source in data_source_series:
                series_data = self.cubejs_client.fetch_data(tenant_code, json.loads(data_source.query), filter_list)

                series_name = data_source.name if data_source.name else 'common'
                if series_name not in field_mappings:
                    field_mappings[series_name] = {}

                # replace keys with given mappings
                for data_point in series_data:
                    for key in list(data_point.keys()):
                        mapped_key = field_mappings[series_name].get(key, field_mappings['common'].get(key))
                        if mapped_key:
                            data_point[mapped_key] = data_point.pop(key)

                result_series.append([data_point for data_point in series_data
                                      if ('name' in data_point and data_point['name'] is not None)
                                      or ('x_value' in data_point and data_point['x_value'] is not None)])

            # Sample result - list of series
            # [
            #   [ {"x":1,"y":1}, {"x":2,"y":4}, {"x":3,"y":9} ],
            #   [ {"x":1,"y":1}, {"x":2,"y":8}, {"x":3,"y":27} ]
            # ]

        return result_series
