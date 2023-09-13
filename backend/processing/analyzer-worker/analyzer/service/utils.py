import json
import logging
import time

logger = logging.getLogger(__name__)

from itertools import chain


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
