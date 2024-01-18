from typing import List, Tuple, Dict

from service.app.data.utils.text_processor import clean_text
from service.app.data.utils.word_freq_utils import TextWordWeight
from service.app.visualization.dynamic_dashboard.handler._common_dashboard_handle import get_query_result, get_field_element, get_filter_value
from service.app.visualization.model.chart_models import FilterDO, DataSourceType
from service.common.config.app_settings import app_settings
from service.common.models import FieldValue


def generate_freq_map(lang_code: str, text: str) -> List[Tuple[str, int]]:
    frequency_count: Dict[str, int] = {}
    word_list = text.split()
    for word in word_list:
        cleaned_text = clean_text(text=word, deep_clean=True, lang_code=lang_code)
        if cleaned_text.strip() != "":
            if word in frequency_count:
                frequency_count[word] += 1
            else:
                frequency_count[word] = 1

    return sorted(frequency_count.items(), key=lambda item: item[1], reverse=True)


def handle_word_cloud(component_inputs: List[FieldValue],
                      filter_list: List[FilterDO], tenant_code: str):
    lang_code = str(get_filter_value(filter_list, 'lang') or 'en')
    query_obj = get_field_element(component_inputs, "query")
    if query_obj:
        query = query_obj.value
        component_inputs.remove(query_obj)
        results = get_query_result(
            data_source_type=DataSourceType.CUBE_JS,
            tenant_code=tenant_code,
            query=query,
            filter_list=filter_list,
            is_timeseries=False)

        text = "\n".join([result[0] for result in results[1:]])
        cleaned_text = clean_text(text, True).lower()

        word_cloud = [
                         TextWordWeight(term=word, weight=frequency)
                         for word, frequency in generate_freq_map(lang_code=lang_code, text=cleaned_text)
                     ][: app_settings.MAX_WORD_COUNT]

        component_inputs.append(FieldValue(field="word_cloud", value=word_cloud))
