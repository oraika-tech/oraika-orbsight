from typing import List

from ...dynamic_dashboard.common.utility import get_field_element
from ...model.chart_models import DataSourceType, FilterDO
from ...model.dashboard_models import FieldValue


def handle_live_feed(data_view_manager, component_inputs: List[FieldValue], filter_list: List[FilterDO],
                     tenant_code: str):
    query_obj = get_field_element(component_inputs, "query")
    if query_obj:
        query = query_obj.value
        component_inputs.remove(query_obj)
        filter_list.append(FilterDO(
            name='period',
            values=['Last 30 days']
        ))
        results = data_view_manager.get_query_result(
            data_source_type=DataSourceType.CUBE_JS,
            tenant_code=tenant_code,
            query=query,
            filter_list=filter_list,
            is_timeseries=False)
        component_inputs.append(FieldValue(field="live_feeds", value=results))
