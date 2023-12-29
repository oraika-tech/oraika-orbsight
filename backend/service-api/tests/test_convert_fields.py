import pytest

from service.common.utils.reflection_utils import convert_fields


def test_convert_field_map_with_flat_structure():
    field_map = {
        "old_key1": "new_key1",
        "old_key2": "new_key2"
    }
    input_object = {
        "old_key1": "value1",
        "old_key2": "value2",
        "old_key3": "value3"
    }
    expected_result = {
        "new_key1": "value1",
        "new_key2": "value2",
        "old_key3": "value3"
    }
    assert convert_fields(field_map, input_object) == expected_result


def test_convert_field_map_with_nested_structure():
    field_map = {
        "old_key1": "new_key1",
        "old_key2": {
            "nested_old_key1": "nested_new_key1"
        }
    }
    input_object = {
        "old_key1": "value1",
        "old_key2": {
            "nested_old_key1": "nested_value1",
            "nested_old_key2": "nested_value2"
        },
        "old_key3": "value3"
    }
    expected_result = {
        "new_key1": "value1",
        "nested_new_key1": "nested_value1",
        "old_key2": {
            "nested_old_key1": "nested_value1",
            "nested_old_key2": "nested_value2"
        },
        "old_key3": "value3"
    }
    assert convert_fields(field_map, input_object) == expected_result


def test_convert_field_map_with_empty_field_map():
    field_map = {}
    input_object = {
        "old_key1": "value1",
        "old_key2": "value2",
        "old_key3": "value3"
    }
    expected_result = {
        "old_key1": "value1",
        "old_key2": "value2",
        "old_key3": "value3"
    }
    assert convert_fields(field_map, input_object) == expected_result


def test_convert_field_map_with_empty_input_object():
    field_map = {
        "old_key1": "new_key1",
        "old_key2": "new_key2"
    }
    input_object = {}
    expected_result = {}
    assert convert_fields(field_map, input_object) == expected_result


def test_convert_field_map_with_none_input_object():
    field_map = {
        "old_key1": "new_key1",
        "old_key2": "new_key2"
    }
    input_object = None
    expected_result = {}
    assert convert_fields(field_map, input_object) == expected_result


@pytest.mark.parametrize("field_map, input_object", [
    (None, {"old_key1": "value1", "old_key2": "value2", "old_key3": "value3"}),
    ({"old_key1": "new_key1", "old_key2": "new_key2"}, None),
    (None, None)
])
def test_convert_field_map_with_none_field_map_or_input_object(field_map, input_object):
    expected_result = input_object if input_object and not field_map else {}
    assert convert_fields(field_map, input_object) == expected_result
