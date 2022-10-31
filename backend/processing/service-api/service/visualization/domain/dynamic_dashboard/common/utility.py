from typing import List

from service.visualization.domain.model.dashboard_models import FieldValue


def get_field_element(component_inputs: List[FieldValue], field_name: str):
    for input_obj in component_inputs:
        if input_obj.field == field_name:
            return input_obj
    return None


def get_field_value(component_inputs: List[FieldValue], field_name: str):
    element = get_field_element(component_inputs, field_name)
    return element.value if element else None
