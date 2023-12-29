from typing import List, Type, TypeVar, Any, Optional

T = TypeVar('T')


def convert_dict_to_hierarchy(input_dict):
    result = {}
    for key, value in input_dict.items():
        keys = key.split('.')
        d = result
        for k in keys[:-1]:
            if k not in d:
                d[k] = {}
            d = d[k]
        d[keys[-1]] = value
    return result


def convert_fields(field_map: dict[str, str], input_object: Any, only_mapped_field: bool = False) -> dict[str, Any]:
    if not input_object:
        return {}

    if not field_map:
        return input_object

    field_map_hierarchy = convert_dict_to_hierarchy(field_map)
    result = {}
    object_dict = input_object if isinstance(input_object, dict) else input_object.dict()
    for key, value in object_dict.items():
        if key in field_map_hierarchy:
            field_map_value = field_map_hierarchy[key]
            if isinstance(field_map_value, str):
                result[field_map_value] = value
            else:
                nested_result = convert_fields(field_map_value, value, True)
                result.update(nested_result)
                result[key] = value
        elif not only_mapped_field:
            result[key] = value

    return result


def convert_model(input_object: Any, return_type: Type[T], field_map: Optional[dict[str, Any]] = None) -> Optional[T]:
    if not input_object:
        return None
    if field_map is None:
        field_map = {}
    data = input_object if isinstance(input_object, dict) else input_object.dict()
    mapped_data = convert_fields(field_map, data)
    return return_type(**mapped_data)


def convert_models(input_objects: List[Any], return_type: Type[T], field_map: Optional[dict[str, str]] = None) -> List[T]:
    if field_map is None:
        field_map = {}
    output_objects = [convert_model(input_object, return_type, field_map) for input_object in input_objects]
    return [output_object for output_object in output_objects if output_object]
