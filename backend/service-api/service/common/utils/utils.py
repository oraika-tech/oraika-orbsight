import json
import logging
import time
from itertools import chain
from typing import Any, List, Tuple, Optional, Dict

logger = logging.getLogger(__name__)


def dict_get(dict_obj: Optional[Dict[str, Any]], key: str) -> Optional[Any]:
    if not dict_obj:
        return None
    return dict_obj.get(key)


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


def merge_dict_arrays_comp(input_dict):
    return list(chain.from_iterable(input_dict.values()))


def intersect_arrays(array1, array2):
    return [item for item in array1 if item in array2]


def split_array(arr, batch_size):
    return [arr[i:i + batch_size] for i in range(0, len(arr), batch_size)]


def flatten_array(nested_arr):
    return [elem for sublist in nested_arr for elem in sublist]


def retry(operation, args, max_retries=3, delay=1) -> str:
    retries = 0
    while True:
        try:
            return operation(*args)
        except Exception as e:
            logger.error("Error occurred: %s", e)
            retries += 1
            logger.info(f"Retrying ({retries}/{max_retries}) in {delay} second(s)...")
            time.sleep(delay)
            delay *= 2
            if retries > max_retries:
                logger.error("Operation failed after %d retries.", max_retries)
                raise e


def extract_json(input_text):
    # Find the first opening bracket or brace
    start_index = min(input_text.find('['), input_text.find('{'))
    if start_index == -1:
        return "No JSON start found in the input text"

    # Find the last closing bracket or brace
    end_index = max(input_text.rfind(']'), input_text.rfind('}'))
    if end_index == -1:
        return "No JSON end found in the input text"

    # Extract the substring between the start and end indices
    json_string = input_text[start_index:end_index + 1]

    # Check if the extracted string is valid JSON
    try:
        return json.loads(json_string)
    except json.JSONDecodeError:
        return "No valid JSON found in the input text"
