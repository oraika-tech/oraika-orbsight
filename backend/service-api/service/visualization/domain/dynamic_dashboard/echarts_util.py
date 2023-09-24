import copy
import logging
from typing import List, Optional

from pydantic import BaseModel

logger = logging.getLogger(__name__)


class EchartsDataset(BaseModel):
    dimensions: Optional[List[str]]
    source: List[list]


def get_dataset_from_series_data():
    pass


def get_pivoted_chart_series():
    # duplicate series per pivot value
    pass


def merge_dataset_and_chart_option():
    pass


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


def remove_metric_name(dimension: str):
    if '.' in dimension:
        return '.'.join(dimension.split('.')[:-1])
    else:
        return dimension


def echarts_option_translation_update(echarts_option: dict, series_data_list: List[List]):
    echarts_option['dataset'] = [EchartsDataset(source=series_data) for series_data in series_data_list]
    for i in range(min(len(series_data_list), len(echarts_option['series']))):
        series = echarts_option['series'][i]

        isFirst = True
        series_original = copy.copy(series)
        for dimension in series_data_list[i][0][1:]:
            if isFirst:
                current_series = series
            else:
                current_series = copy.copy(series_original)
                echarts_option['series'].append(current_series)
            current_series['name'] = remove_metric_name(dimension)
            current_series['datasetIndex'] = i
            if 'encode' in current_series:  # currently, used for line graphs
                encode = copy.copy(current_series['encode'])
                encode['y'] = dimension
                current_series['encode'] = encode
            isFirst = False
