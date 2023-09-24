from typing import List, Optional

from service.visualization.domain.model.chart_models import FilterDO
from service.visualization.domain.model.dashboard_models import FieldValue


def get_field_element(component_inputs: List[FieldValue], field_name: str):
    for input_obj in component_inputs:
        if input_obj.field == field_name:
            return input_obj
    return None


def get_field_value(component_inputs: List[FieldValue], field_name: str):
    element = get_field_element(component_inputs, field_name)
    return element.value if element else None


def get_filter_element(filter_list: List[FilterDO], field_name: str) -> Optional[FilterDO]:
    for filter_do in filter_list:
        if filter_do.name == field_name:
            return filter_do
    return None


def get_filter_value(filter_list: List[FilterDO], field_name: str) -> Optional[List[str]]:
    element = get_filter_element(filter_list, field_name)
    if not element or not element.values or len(element.values) == 0:
        return None
    return element.values
