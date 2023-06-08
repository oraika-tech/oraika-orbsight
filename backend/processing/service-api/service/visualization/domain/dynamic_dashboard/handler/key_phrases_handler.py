from typing import List

from service.data import TextProcessor
from service.data.domain.model.key_phrase import KeyPhraseWeight
from ...dynamic_dashboard.common.utility import get_field_element, get_filter_value
from ...model.chart_models import DataSourceType, FilterDO
from ...model.dashboard_models import FieldValue

text_processor = TextProcessor()


def get_distance(el):
    return el.distance


def handle_key_phrases(data_view_manager, component_inputs: List[FieldValue],
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
        cleaned_text = text_processor.clean_text(text)

        extracted_phrases = text_processor.extract_key_phrases(
            text=cleaned_text,
            lang_code=lang_code,
            remove_stopwords=False
        )

        key_phrases = [
            KeyPhraseWeight(phrase=key_phrase, distance=distance)
            for key_phrase, distance in extracted_phrases.items()
        ]
        key_phrases.sort(key=get_distance, reverse=True)

        component_inputs.append(FieldValue(field="key_phrases", value=key_phrases))
