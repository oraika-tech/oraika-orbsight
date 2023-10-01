import json
import logging
from typing import List

from service.app.visualization.dynamic_dashboard.handler._common_dashboard_handle import get_query_result, get_domain_field, combine_series, \
    get_field_value
from service.app.visualization.model.chart_models import FilterDO, DataTransformerMetaDO, FieldPivotDO, DataSourceType
from service.common.models import FieldValue

logger = logging.getLogger(__name__)


def replace_headers_with_alias(headers, header_aliases):
    for column_index, column_name in enumerate(headers):
        for key_column in header_aliases:
            if key_column['column'] == column_name:
                headers[column_index] = key_column['header']


def handle_simple_table(component_inputs: List[FieldValue],
                        filter_list: List[FilterDO], tenant_code: str):
    data_config = get_field_value(component_inputs, "data_config")

    result_series = []
    for series in data_config['series']:
        logger.debug("Chart DB Query:%s", series['query'])

        data_transformer_meta = None
        if 'pivot_columns' in series:
            data_transformer_meta = DataTransformerMetaDO(
                field_pivoting=[FieldPivotDO(columns=series['pivot_columns'])])

        dataset_result = get_query_result(
            data_source_type=DataSourceType.CUBE_JS,
            tenant_code=tenant_code,
            query=json.loads(series['query']),
            filter_list=filter_list,
            default_value=series.get('default_value'),
            is_timeseries=False,
            series_name=series['name'],
            data_transformer_meta=data_transformer_meta
        )
        replace_headers_with_alias(dataset_result[0], series['header_alias'])
        result_series.append(dataset_result)

    for key_column in data_config['key_columns']:
        domain_column = get_domain_field(key_column['column'])
        if domain_column:
            key_column['column'] = domain_column

    key_column = data_config['key_columns'][0]['column']
    key_columns_index = [index
                         for series_data in result_series
                         for index, header_column in enumerate(series_data[0])
                         if header_column == key_column]

    default_values = [series.get('default_value') for series in data_config['series']]
    logger.debug("Default Values: %s", default_values)
    table_data = combine_series(result_series, key_columns_index, default_values)
    replace_headers_with_alias(table_data[0], data_config['key_columns'])

    column_definition = [
        {
            'accessorKey': column_name.lower().replace(' ', '_'),
            'header': column_name,
            'minSize': max(map(lambda e: len(str(e[i])), table_data)) * 10  # calculate min width based on data
        }
        for i, column_name in enumerate(table_data[0])
    ]

    component_inputs.append(FieldValue(field='table_data', value=table_data))
    component_inputs.append(FieldValue(field='column_definition', value=column_definition))
