import copy
import logging
from typing import List

logger = logging.getLogger(__name__)


def group_by(obj_list: List[dict], field_name: str) -> dict[str, List]:
    groups: dict[str, List] = {'common': []}
    for element in obj_list:
        if field_name in element:
            field_value = element[field_name]
            if field_value in groups:
                groups[field_value].append(element)
            else:
                groups[field_value] = [element]
        else:
            groups['common'].append(element)
    return groups


def echarts_option_translation_update(echarts_option: dict, series_data_list: List[List[dict]]):
    for i in range(min(len(series_data_list), len(echarts_option['series']))):
        series = echarts_option['series'][i]
        if series['type'] == 'line':
            data_series = group_by(series_data_list[i], 'name')
            isFirst = True
            series_original = copy.copy(series)
            for name in data_series:
                if len(data_series[name]) > 0 and (
                        'x_value' not in data_series[name][0] or 'value' not in data_series[name][0]):
                    logging.error(f"Value not present in data {data_series[name][0]}")
                else:
                    data = [[dp['x_value'], dp['value']] for dp in data_series[name]]
                    if isFirst:
                        current_series = series
                    else:
                        current_series = copy.copy(series_original)
                        echarts_option['series'].append(current_series)
                    if name is not None and name.strip() and name != 'common':
                        current_series['name'] = name
                    current_series['data'] = data
                    isFirst = False
        else:
            series['data'] = [dp for dp in series_data_list[i] if len(dp['name'].strip()) > 0]
