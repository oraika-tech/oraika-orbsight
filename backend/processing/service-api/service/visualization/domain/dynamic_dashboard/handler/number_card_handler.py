import json
import logging
from typing import List

from ...dynamic_dashboard.common.utility import get_field_element
from ...model.chart_models import FilterDO, DataSourceType
from ...model.dashboard_models import FieldValue

logger = logging.getLogger(__name__)


def handle_number_card(data_view_manager, component_inputs: List[FieldValue],
                       filter_list: List[FilterDO], tenant_code: str):
    data_config_element = get_field_element(component_inputs, "data_config")

    if data_config_element and data_config_element.value:
        data_config = data_config_element.value

        series_result_value = {}
        for series in data_config['series']:
            logger.debug("Chart DB Query:%s", series['query'])

            result_rows = data_view_manager.get_query_result(
                data_source_type=DataSourceType.CUBE_JS,
                tenant_code=tenant_code,
                query=json.loads(series['query']),
                filter_list=filter_list,
                default_value=series.get('default_value')
            )
            if len(result_rows) >= 2:
                headers = result_rows[0]
                values = result_rows[1]
                for i in range(len(headers)):
                    for header_alias in series['header_alias']:
                        if header_alias['column'] == headers[i]:
                            series_result_value[header_alias['header']] = values[i]

        component_inputs.append(FieldValue(field='template', value=data_config['template']))
        component_inputs.append(FieldValue(field='series_data', value=series_result_value))
        component_inputs.remove(data_config_element)
