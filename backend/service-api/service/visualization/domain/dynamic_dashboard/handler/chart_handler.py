import json
import logging
from typing import List

from service.visualization.domain.dynamic_dashboard.echarts_util import echarts_option_translation_update
from service.visualization.domain.model.chart_models import ChartDBO, FilterDO
from service.visualization.domain.model.dashboard_models import FieldValue

logger = logging.getLogger(__name__)

non_time_series_graphs = {'pie', 'bar'}


def handle_chart(data_view_manager, component_inputs: List[FieldValue], filter_list: List[FilterDO], tenant_code: str,
                 chart: ChartDBO):
    component_inputs.append(FieldValue(
        field='chart_config',
        value={'chart_type': chart.chart_type, 'option': chart.chart_config}
    ))

    is_timeseries = len([series for series in chart.chart_config['series']
                         if series['type'] in non_time_series_graphs]) == 0

    result_series = []
    for data_source in chart.data_source_series:
        logger.debug("Chart DB Query:%s", data_source.query)
        data_query = json.loads(data_source.query)
        data_query['timezone'] = 'Asia/Kolkata'
        dataset_result = data_view_manager.get_query_result(
            data_source_type=chart.data_source_type,
            tenant_code=tenant_code,
            query=data_query,
            filter_list=filter_list,
            default_value=None,
            is_timeseries=is_timeseries,
            series_name=data_source.name,
            data_transformer_meta=chart.data_transformer_meta
        )
        result_series.append(dataset_result)

    if chart.chart_type == 'echarts':
        echarts_option_translation_update(chart.chart_config, result_series)
