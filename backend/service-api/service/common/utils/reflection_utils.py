from typing import List, Type, TypeVar, Any, Optional

T = TypeVar('T')


def convert_model(input_object: Any, return_type: Type[T], field_map=None) -> Optional[T]:
    if not input_object:
        return None
    if field_map is None:
        field_map = {}
    data = input_object if isinstance(input_object, dict) else input_object.dict()
    mapped_data = {field_map.get(k, k): v for k, v in data.items()}
    return return_type(**mapped_data)


def convert_models(input_objects: List[Any], return_type: Type[T], field_map=None) -> List[T]:
    if field_map is None:
        field_map = {}
    output_objects = [convert_model(input_object, return_type, field_map) for input_object in input_objects]
    return [output_object for output_object in output_objects if output_object]
