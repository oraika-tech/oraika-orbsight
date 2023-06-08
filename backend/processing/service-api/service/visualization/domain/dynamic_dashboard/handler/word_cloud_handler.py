import os
from typing import List, Tuple, Dict

from service.data import TextProcessor
from service.data.domain.model.word_freq import TextWordWeight
from ...dynamic_dashboard.common.utility import get_field_element, get_filter_value
from ...model.chart_models import DataSourceType, FilterDO
from ...model.dashboard_models import FieldValue

text_processor = TextProcessor()

max_word_count: int = int(os.environ.get('MAX_WORD_COUNT') or 20)


def generate_freq_map(lang_code: str, text: str) -> List[Tuple[str, int]]:
    frequency_count: Dict[str, int] = {}
    word_list = text.split()
    for word in word_list:
        cleaned_text = text_processor.clean_text(text=word, deep_clean=True, lang_code=lang_code)
        if cleaned_text.strip() != "":
            if word in frequency_count:
                frequency_count[word] += 1
            else:
                frequency_count[word] = 1

    return sorted(frequency_count.items(), key=lambda item: item[1], reverse=True)


def handle_word_cloud(data_view_manager, component_inputs: List[FieldValue],
                      filter_list: List[FilterDO], tenant_code: str):
    lang_code = str(get_filter_value(filter_list, 'lang') or 'en')
    query_obj = get_field_element(component_inputs, "query")
    if query_obj:
        query = query_obj.value
        component_inputs.remove(query_obj)
        results = data_view_manager.get_query_result(
            data_source_type=DataSourceType.CUBE_JS,
            tenant_code=tenant_code,
            query=query,
            filter_list=filter_list,
            is_timeseries=False)

        text = "\n".join([result[0] for result in results[1:]])
        cleaned_text = text_processor.clean_text(text).lower()

        word_cloud = [
                         TextWordWeight(term=word, weight=frequency)
                         for word, frequency in generate_freq_map(lang_code=lang_code, text=cleaned_text)
                     ][: max_word_count]

        component_inputs.append(FieldValue(field="word_cloud", value=word_cloud))
