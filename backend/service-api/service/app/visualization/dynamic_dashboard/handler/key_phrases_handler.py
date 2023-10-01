from typing import List

from service.app.data.utils.key_phrases_utils import KeyPhraseWeight
from service.app.data.utils.text_processor import clean_text, extract_key_phrases
from service.app.visualization.dynamic_dashboard.handler._common_dashboard_handle import get_query_result, get_field_element
from service.app.visualization.model.chart_models import FilterDO, DataSourceType
from service.common.models import FieldValue


def get_distance(el):
    return el.distance


def handle_key_phrases(component_inputs: List[FieldValue],
                       filter_list: List[FilterDO], tenant_code: str):
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
        cleaned_text = clean_text(text)

        extracted_phrases = extract_key_phrases(cleaned_text)

        key_phrases = [
            KeyPhraseWeight(phrase=key_phrase, distance=distance)
            for key_phrase, distance in extracted_phrases.items()
        ]
        key_phrases.sort(key=get_distance, reverse=True)

        component_inputs.append(FieldValue(field="key_phrases", value=key_phrases))
