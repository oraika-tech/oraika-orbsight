import json
import logging
from typing import List, Any
from uuid import UUID

from pydantic import BaseSettings, PrivateAttr

from .base import BasePersistenceManager
from .data_view_manager import DataViewManager
from .echarts_util import echarts_option_translation_update
from .model.chart_models import FilterDO, ChartDBO, DataSourceType
from .model.dashboard_models import DashboardDO, FieldValue
from ...common.utils import dict_group_by

logger = logging.getLogger(__name__)


class DynamicDashboardManager(BaseSettings):
    persistence_manager: BasePersistenceManager
    data_view_manager: DataViewManager
    _non_time_series_graphs: set = PrivateAttr()

    def __init__(self, **data: Any):
        super().__init__(**data)
        self._non_time_series_graphs = {'pie', 'bar'}

    @staticmethod
    def get_field_element(component_inputs: List[FieldValue], field_name: str):
        for input_obj in component_inputs:
            if input_obj.field == field_name:
                return input_obj
        return None

    def get_field_value(self, component_inputs: List[FieldValue], field_name: str):
        element = self.get_field_element(component_inputs, field_name)
        return element.value if element else None

    def handle_chart(self, component_inputs: List[FieldValue], filter_list: List[FilterDO], tenant_code: str,
                     chart: ChartDBO):
        component_inputs.append(FieldValue(
            field='chart_config',
            value={'chart_type': chart.chart_type, 'option': chart.chart_config}
        ))

        is_timeseries = len([series for series in chart.chart_config['series']
                             if series['type'] in self._non_time_series_graphs]) == 0

        result_series = []
        for data_source in chart.data_source_series:
            logger.debug("Chart DB Query:%s", data_source.query)
            dataset_result = self.data_view_manager.get_query_result(
                chart.data_source_type,
                tenant_code,
                json.loads(data_source.query),
                filter_list,
                is_timeseries,
                data_source.name,
                chart.data_transformer_meta
            )
            result_series.append(dataset_result)

        if chart.chart_type == 'echarts':
            echarts_option_translation_update(chart.chart_config, result_series)

    def handle_filter_panel(self, component_inputs: List[FieldValue], filter_list: List[FilterDO], tenant_code: str):
        filter_map = {filter_obj.name: filter_obj for filter_obj in filter_list}
        filters = self.get_field_value(component_inputs, "filters")
        for filter_value in filters:
            filter_field = filter_value.get('id')
            if 'data_field' in filter_value:
                data_field = filter_value.pop('data_field')
                if data_field:
                    result = self.data_view_manager.get_unique_field_values(tenant_code, data_field)
                    result_values = [{"code": field_value} for field_value in result if len(field_value.strip()) > 0]
                    filter_value['options'] = [{"code": "all"}]
                    filter_value['options'].extend(result_values)

            filter_value['selectedValue'] = {'code': filter_map[filter_field].values[0]} \
                if filter_field in filter_map \
                else filter_value['defaultValue']

    def handle_live_feed(self, component_inputs: List[FieldValue], filter_list: List[FilterDO], tenant_code: str):
        query_obj = self.get_field_element(component_inputs, "query")
        if query_obj:
            query = query_obj.value
            component_inputs.remove(query_obj)
            filter_list.append(FilterDO(
                name='period',
                values=['Last 30 days']
            ))
            results = self.data_view_manager.get_query_result(DataSourceType.CUBE_JS, tenant_code,
                                                              query, filter_list, is_timeseries=False)
            component_inputs.append(FieldValue(field="live_feeds", value=results))

    def handle_simple_table(self, component_inputs: List[FieldValue], filter_list: List[FilterDO], tenant_code: str):
        pass

    def handle_number_card(self, component_inputs: List[FieldValue], filter_list: List[FilterDO], tenant_code: str):
        pass

    def get_updated_dashboard_info(self, tenant_id: UUID, tenant_code: str, dashboard: DashboardDO,
                                   filter_list: List[FilterDO], include_components: bool):
        if not include_components:
            dashboard.component_layout = None
            return dashboard

        dashboard.component_layout.components = [component
                                                 for component in dashboard.component_layout.components
                                                 if not component.disabled]

        # section for batch processing by type
        charts = {}
        components_by_type = dict_group_by(
            [component.dict() for component in dashboard.component_layout.components if component.disabled is not True],
            'type')
        for component_type, component_list in components_by_type.items():
            if component_type == 'chart':
                chart_ids = [component['identifier']
                             for component in component_list
                             if component['identifier'] is not None]
                charts = self.persistence_manager.get_charts_by_ids(tenant_id, chart_ids)

        # section for single processing by type
        for component in dashboard.component_layout.components:
            if component.inputs is None:
                component.inputs = []
            if component.type == 'chart':
                self.handle_chart(component.inputs, filter_list, tenant_code, charts[component.identifier])
            elif component.type == 'react-component':
                if component.name == 'FilterPanel':
                    self.handle_filter_panel(component.inputs, filter_list, tenant_code)
                elif component.name == 'LiveFeedTable':
                    self.handle_live_feed(component.inputs, filter_list, tenant_code)
                elif component.name == 'SimpleTable':
                    self.handle_simple_table(component.inputs, filter_list, tenant_code)
                elif component.name == 'NumberCard':
                    self.handle_number_card(component.inputs, filter_list, tenant_code)

        return dashboard
