from typing import List

from service.app.visualization.dynamic_dashboard.handler._common_dashboard_handle import get_unique_field_values, get_field_value
from service.app.visualization.model.chart_models import FilterDO
from service.common.models import FieldValue


def handle_filter_panel(component_inputs: List[FieldValue], filter_list: List[FilterDO],
                        tenant_code: str):
    filter_map = {filter_obj.name: filter_obj for filter_obj in filter_list}
    filters = get_field_value(component_inputs, "filters")
    for filter_value in filters:
        filter_field = filter_value.get('id')
        if 'data_field' in filter_value:
            data_field = filter_value.pop('data_field')
            if data_field:
                result = get_unique_field_values(tenant_code, data_field)
                result_values = [{"code": field_value} for field_value in result if len(field_value.strip()) > 0]
                filter_value['options'] = [{"code": "all"}]
                filter_value['options'].extend(result_values)

        filter_value['selectedValue'] = filter_value['defaultValue']
        if filter_field in filter_map:
            filter_values = filter_map[filter_field].values
            if filter_values:
                filter_value['selectedValue'] = {'code': filter_values[0]}
