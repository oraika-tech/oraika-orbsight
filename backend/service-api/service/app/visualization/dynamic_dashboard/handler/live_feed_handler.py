from typing import List

from service.app.visualization.dynamic_dashboard.handler._common_dashboard_handle import get_query_result, get_field_element
from service.app.visualization.model.chart_models import FilterDO, DataSourceType
from service.common.models import FieldValue


def handle_live_feed(component_inputs: List[FieldValue], filter_list: List[FilterDO],
                     tenant_code: str):
    query_obj = get_field_element(component_inputs, "query")
    if query_obj:
        query = query_obj.value
        component_inputs.remove(query_obj)
        filter_list.append(FilterDO(
            name='period',
            values=['Last 30 days']
        ))
        results = get_query_result(
            data_source_type=DataSourceType.CUBE_JS,
            tenant_code=tenant_code,
            query=query,
            filter_list=filter_list,
            is_timeseries=False)
        component_inputs.append(FieldValue(field="live_feeds", value=results))
