from typing import List

from ..common.utility import get_field_value
from ...model.chart_models import FilterDO
from ...model.dashboard_models import FieldValue


def handle_filter_panel(data_view_manager, component_inputs: List[FieldValue], filter_list: List[FilterDO],
                        tenant_code: str):
    filter_map = {filter_obj.name: filter_obj for filter_obj in filter_list}
    filters = get_field_value(component_inputs, "filters")
    for filter_value in filters:
        filter_field = filter_value.get('id')
        if 'data_field' in filter_value:
            data_field = filter_value.pop('data_field')
            if data_field:
                result = data_view_manager.get_unique_field_values(tenant_code, data_field)
                result_values = [{"code": field_value} for field_value in result if len(field_value.strip()) > 0]
                filter_value['options'] = [{"code": "all"}]
                filter_value['options'].extend(result_values)

        filter_value['selectedValue'] = {'code': filter_map[filter_field].values[0]} \
            if filter_field in filter_map \
            else filter_value['defaultValue']
