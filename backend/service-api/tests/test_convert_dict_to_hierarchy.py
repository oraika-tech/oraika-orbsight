from service.common.utils.reflection_utils import convert_dict_to_hierarchy


def test_convert_dict_to_hierarchy_with_empty_dict():
    input_dict = {}
    expected_result = {}
    assert convert_dict_to_hierarchy(input_dict) == expected_result


def test_convert_dict_to_hierarchy_with_flat_structure():
    input_dict = {"key1": "value1", "key2": "value2"}
    expected_result = {"key1": "value1", "key2": "value2"}
    assert convert_dict_to_hierarchy(input_dict) == expected_result


def test_convert_dict_to_hierarchy_with_nested_structure():
    input_dict = {"key1.subkey1": "value1", "key2.subkey2": "value2"}
    expected_result = {"key1": {"subkey1": "value1"}, "key2": {"subkey2": "value2"}}
    assert convert_dict_to_hierarchy(input_dict) == expected_result


def test_convert_dict_to_hierarchy_with_mixed_structure():
    input_dict = {"key1": "value1", "key2.subkey2": "value2"}
    expected_result = {"key1": "value1", "key2": {"subkey2": "value2"}}
    assert convert_dict_to_hierarchy(input_dict) == expected_result


def test_convert_dict_to_hierarchy_with_multilevel_nested_structure():
    input_dict = {"key1.subkey1.subsubkey1": "value1", "key2.subkey2.subsubkey2": "value2"}
    expected_result = {"key1": {"subkey1": {"subsubkey1": "value1"}}, "key2": {"subkey2": {"subsubkey2": "value2"}}}
    assert convert_dict_to_hierarchy(input_dict) == expected_result
