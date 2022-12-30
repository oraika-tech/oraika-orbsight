import time
from typing import Any, List, Tuple


def search_dict(partial: Any, search_key: str):
    stack = [partial]
    while stack:
        current_item = stack.pop()
        if isinstance(current_item, dict):
            for key, value in current_item.items():
                if key == search_key:
                    yield value
                else:
                    stack.append(value)
        elif isinstance(current_item, list):
            for value in current_item:
                stack.append(value)


def to_camel_case(snake_str):
    components = snake_str.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])


def dict_replace_keys(obj, key_map: dict[str, str]):
    if isinstance(obj, dict):
        for key in obj:
            dict_replace_keys(obj[key], key_map)
            if key in key_map:
                obj[key_map[key]] = obj.pop(key)
    elif isinstance(obj, list):
        for element in obj:
            dict_replace_keys(element, key_map)


def dict_group_by(dict_objects: List[dict], field_name: str) -> dict[str, List[dict]]:
    result_dict: dict[str, list[Any]] = {}
    for dict_obj in dict_objects:
        if field_name not in dict_obj:
            continue
        field_value = dict_obj[field_name]
        if field_value not in result_dict:
            result_dict[field_value] = []
        result_dict[field_value].append(dict_obj)
    return result_dict


def dedup_list(string_list: List[str]):
    return list(dict.fromkeys(string_list))


def list_split_by_condition(given_list: List, condition_fx) -> Tuple[list, list]:
    true_list = []
    false_list = []
    for element in given_list:
        if condition_fx(element):
            true_list.append(element)
        else:
            false_list.append(element)
    return true_list, false_list


def to_space_camel_case(sentence: str):
    words = sentence.split(' ')
    titled_words = [word.title() for word in words]
    return ' '.join(titled_words)


def now_epoch():
    return int(time.time())
