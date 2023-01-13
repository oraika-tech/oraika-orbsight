import logging
from functools import reduce
from typing import Optional, List, Any, Dict

from pydantic import BaseSettings, PrivateAttr

from service.common.utils import dedup_list, list_split_by_condition, to_space_camel_case
from service.visualization.domain.model.chart_models import DatasetResult, DataTransformerMetaDO, \
    DataSourceType, FieldPivotDO
from service.visualization.domain.model.chart_models import FilterDO
from service.visualization.domain.model.common_models import SortOrder, OrderData
from service.visualization.persistence.cubejs_client import CubejsClient

logger = logging.getLogger(__name__)


class DataViewManager(BaseSettings):
    _main_view_name: str = PrivateAttr()
    _field_mapping_domain_to_db: dict[str, str] = PrivateAttr()
    _field_mapping_db_to_domain: dict[str, str] = PrivateAttr()
    _time_field_name: set[str] = PrivateAttr()
    cubejs_client: CubejsClient

    def __init__(self, **data: Any):
        super().__init__(**data)

        self._main_view_name = 'ProcessedDataViewV1.'
        self._field_mapping_domain_to_db = {
            'categories': 'Categories.category',
            'category': 'Categories.category',
            'taxonomies': 'TaxonomyTags.taxonomyTag',
            'taxonomy': 'TaxonomyTags.taxonomyTag',  # order matters - db_to_domain only use last "key" for same "value"
            'term': 'TaxonomyTerms.taxonomyTerm',
            'emotion': self._main_view_name + 'emotion',
            'observerType': self._main_view_name + 'observerType',
            'observer': self._main_view_name + 'observerName',
            'entity': self._main_view_name + 'entityName',
            'lang': self._main_view_name + 'textLang',
            'author': self._main_view_name + 'authorName',
            'Unique Users': self._main_view_name + 'uniqueAuthorCount',
            'Unique Conversations': self._main_view_name + 'uniqueConversationCount'
        }
        self._field_mapping_db_to_domain = {value: key for key, value in self._field_mapping_domain_to_db.items()}
        self._time_field_name = {'period', 'interval'}

    def get_domain_field(self, db_field: str) -> str:
        return self._field_mapping_db_to_domain.get(
            db_field,
            db_field.replace(self._main_view_name, ''))

    def get_db_field(self, domain_field: str) -> str:
        return self._field_mapping_domain_to_db.get(
            domain_field,
            self._main_view_name + domain_field)

    def fetch_data(self, tenant_code: str, query: dict) -> List[dict]:
        return self.cubejs_client.fetch_data(tenant_code, query)

    def get_unique_field_values(self, tenant_code, field_name) -> List[str]:
        db_field = self.get_db_field(field_name)
        query = {"dimensions": [db_field]}
        result = self.cubejs_client.fetch_data(tenant_code, query)
        return [field_value[db_field] for field_value in result if len(field_value[db_field].strip()) > 0]

    @staticmethod
    def int_sum(v1, v2):
        v1 = v1 or 0
        v2 = v2 or 0
        return int(v1) + int(v2)

    @staticmethod
    def str_concat(v1, v2):
        v1 = v1 or ''
        v2 = v2 or ''
        return v1 + v2

    def pivot_result(self, results: List[List], field_pivoting: FieldPivotDO,
                     dimension_fields: List[str], sort_order: Optional[SortOrder] = None, default_value=None):
        """
            If given columns
                [column1, column2, column3, column4, column5]
                  value1,  value2,  value3,  value4,  value5
            assuming pivot columns
                [column3, column4]
            pivoted columns will be
                [column1, value2.value3.column4, value2.value3.column5]
                  value1,                value4,                value5

            pc: pivot column
            npc: non pivot column
            npv: non pivot value
        """
        pivoted_result_map: Dict[str, Dict[str, str]] = {}
        pivoted_dimensions: Dict[str, int] = {}
        df_index = {field: i for i, field in enumerate(dimension_fields)}
        non_pivot_fields = [field for field in dimension_fields[1:] if field not in field_pivoting.columns]
        for record in results:
            x_dimension_value = record[0]
            if x_dimension_value not in pivoted_result_map:
                pivoted_result_map[x_dimension_value] = {}

            row = pivoted_result_map[x_dimension_value]
            for non_pivot_field in non_pivot_fields:
                pivot_values = [record[df_index[pivot_field]]
                                for pivot_field in field_pivoting.columns
                                if record[df_index[pivot_field]]]
                pivot_column = '.'.join(pivot_values + [non_pivot_field])
                if pivot_column in pivoted_dimensions:
                    pivoted_dimensions[pivot_column] += 1
                else:
                    pivoted_dimensions[pivot_column] = 0
                row[pivot_column] = record[df_index[non_pivot_field]]  # pc1.pc2.npc1 = npv1

        tabular_results = [
            [x_column_value] +
            [other_values.get(column_names, default_value) for column_names in pivoted_dimensions.keys()]
            for x_column_value, other_values in pivoted_result_map.items()
        ]
        result_columns = [dimension_fields[0]] + list(pivoted_dimensions.keys())

        if sort_order and len(sort_order.order):
            order_columns_index = [i
                                   for i, result_column in enumerate(result_columns)
                                   for order_data in sort_order.order
                                   if result_column.endswith(order_data.field)]

            reduction_fx = self.int_sum if sort_order.is_all_numbers else self.str_concat

            def key_function(row_value: List):
                order_values = [row_value[i] for i in order_columns_index]
                return reduce(reduction_fx, order_values)

            tabular_results.sort(key=key_function, reverse=sort_order.order[0].is_reverse)

        return DatasetResult(dimensions=result_columns, results=tabular_results).get_dataset()

    @staticmethod
    def normal_result(results: List[dict], dimension_fields: List[str]):
        return DatasetResult(
            dimensions=dimension_fields,
            results=[
                [result.get(dimension) for dimension in dimension_fields]
                for result in results
            ]
        )

    @staticmethod
    def get_time_dimensions(query: dict) -> List[str]:
        result_dimensions = []
        if 'timeDimensions' in query:
            for time_dimension in query.get('timeDimensions', []):
                if time_dimension and 'dimension' in time_dimension:
                    result_dimensions.append(time_dimension['dimension'])
        return result_dimensions

    @staticmethod
    def get_result_for_dimension(results, db_dimensions, default_value):
        return [
            [record.get(db_dimensions, default_value) for db_dimensions in db_dimensions]
            for record in results
        ]

    @staticmethod
    def get_code_to_daterange(code: str):
        return to_space_camel_case(code.replace('-', ' '))

    def create_time_dimension(self, time_filters: List[FilterDO], is_timeseries: bool):
        time_dimension = {
            "dimension": "ProcessedDataViewV1.eventTime",
            "dateRange": "Last 7 days"
        }
        for time_filter in time_filters:
            if time_filter.values:
                if time_filter.name == "period":
                    time_dimension["dateRange"] = self.get_code_to_daterange(time_filter.values[0])
                elif is_timeseries and time_filter.name == "interval":
                    time_dimension["granularity"] = time_filter.values[0]
        if is_timeseries and "granularity" not in time_dimension:
            time_dimension["granularity"] = "day"
        return time_dimension

    def get_query_result(self, data_source_type: DataSourceType, tenant_code: str, query: dict,
                         filter_list: List[FilterDO], default_value=None, is_timeseries=False,
                         series_name: Optional[str] = None,
                         data_transformer_meta: Optional[DataTransformerMetaDO] = None) -> List[List]:

        time_filters, dimension_filters = list_split_by_condition(
            filter_list, lambda filter_do: filter_do.name in self._time_field_name)

        query["timeDimensions"] = [self.create_time_dimension(time_filters, is_timeseries)]

        if dimension_filters:
            filters = [{'member': self.get_db_field(filterDO.name),
                        'values': filterDO.values,
                        'operator': filterDO.operator}
                       for filterDO in dimension_filters]
            if "filters" in query:
                query["filters"] += filters
            else:
                query["filters"] = filters

        results = []
        logger.debug('Final Query:%s', query)
        if data_source_type == DataSourceType.CUBE_JS:
            results = self.cubejs_client.fetch_data(tenant_code, query)

        time_dimension = self.get_time_dimensions(query) if is_timeseries else []
        db_dimensions = dedup_list(time_dimension + query.get('dimensions', []) + query.get('measures', []))
        dimension_fields = [self.get_domain_field(field) for field in db_dimensions]
        domain_results = self.get_result_for_dimension(results, db_dimensions, default_value)

        field_pivoting = None
        if data_transformer_meta and data_transformer_meta.field_pivoting:
            for fp in data_transformer_meta.field_pivoting:
                if fp.series_name:
                    if fp.series_name == series_name:
                        field_pivoting = fp
                else:
                    if not field_pivoting:
                        field_pivoting = fp

        if field_pivoting:
            order_dimensions = self.get_sort_order_from_query(query)
            return self.pivot_result(domain_results, field_pivoting, dimension_fields, order_dimensions, default_value)

        return DatasetResult(dimensions=dimension_fields, results=domain_results).get_dataset()

    def get_sort_order_from_query(self, query: dict):
        ordering: Optional[dict] = query.get('order')
        measures: List = query.get('measures', [])

        if not ordering:
            return None

        return SortOrder(
            order=[OrderData(field=self.get_domain_field(field), is_reverse=(order == 'desc'))
                   for field, order in ordering.items()],
            is_all_numbers=all(field in measures for field in ordering) if measures else False
        )

    @staticmethod
    def combine_series(series_list: List[List[List]],
                       key_columns_index: Optional[List[int]] = None,
                       series_default_values: Optional[list] = None):
        """
        :param series_list:  List of series. Each series table with list of rows. Each row is list of columns
        :param key_columns_index: Column index of key column in each series
        :param series_default_values: List of default value of each series
        :return:
        """

        if not key_columns_index:  # by default, pick first column as x-axis
            key_columns_index = [0] * len(series_list)

        series_map_list: List[dict] = [
            {
                row.pop(key_columns_index[series_index]): row
                for row in series
            }
            for series_index, series in enumerate(series_list)
        ]

        x_values = list(dict.fromkeys([x_column for series_map in series_map_list for x_column in series_map.keys()]))

        combined_series_map: Dict[str, List[str]] = {}

        series_col_nos = [len(series_map) for series_map in series_map_list]

        default_values = series_default_values or [None] * len(series_list)

        for x_value in x_values:
            combined_series_map[x_value] = []
            for i, series_map in enumerate(series_map_list):
                if x_value in series_map:
                    row_values = series_map[x_value]
                else:
                    row_values = [default_values[i]] * series_col_nos[i]
                combined_series_map[x_value].extend(row_values)

        return [
            [x_value] + other_values
            for x_value, other_values in combined_series_map.items()
        ]
