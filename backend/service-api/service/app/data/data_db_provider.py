import copy
from datetime import datetime
from typing import Any, Dict, List, Optional

from service.app.data.data_models import (AnalysisData, DataEntity, DataTerm,
                                          RawData, TextAnalysisData)
from service.common.infra.db.repository.data.processed_data_repository import \
    update_structured_data
from service.common.infra.db.repository.data.processed_view_repository import (
    get_distinct_entity_names, get_distinct_languages,
    get_distinct_observer_types, get_distinct_terms, get_processed_data_view)
from service.common.infra.db.repository.data.raw_data_repository import \
    RawDataEntity
from service.common.models import DataSourceType, FilterQueryParams
from service.common.utils.reflection_utils import convert_models


def convert_to_entity(raw_data: RawData):
    unstructured_data = recursive_serialize(raw_data.unstructured_data) \
        if raw_data.unstructured_data else None
    return RawDataEntity(
        observer_id=raw_data.observer_id,
        reference_id=raw_data.reference_id,
        parent_reference_id=raw_data.parent_reference_id,
        raw_text=raw_data.raw_text,
        # data=json.dumps(raw_data.data, default=datetime_handler),
        unstructured_data=unstructured_data,
        event_time=raw_data.event_time
    )


def convert_from_entity(raw_data_entity: RawDataEntity):
    return RawData(
        identifier=raw_data_entity.identifier,
        observer_id=raw_data_entity.observer_id,
        reference_id=raw_data_entity.reference_id,
        parent_reference_id=raw_data_entity.parent_reference_id,
        raw_text=raw_data_entity.raw_text,
        unstructured_data=raw_data_entity.unstructured_data,
        event_time=raw_data_entity.event_time
    )


def recursive_serialize(original_data: Dict[str, Any]) -> dict:
    data = copy.deepcopy(original_data)

    for key, value in data.items():
        if isinstance(value, datetime):
            data[key] = value.isoformat()
        elif isinstance(value, Dict):
            recursive_serialize(value)

    return data


def get_text_analysis_data_dp(filter_query_params: FilterQueryParams) -> List[TextAnalysisData]:
    processed_data_view = get_processed_data_view(filter_query_params)
    return convert_models(processed_data_view, TextAnalysisData)


def get_data_entities_dp(filter_query_params: FilterQueryParams) -> List[DataEntity]:
    entity_names = get_distinct_entity_names(filter_query_params)
    return [DataEntity(name=name) for name in entity_names]


def get_data_terms_dp(filter_query_params: FilterQueryParams) -> List[DataTerm]:
    terms = get_distinct_terms(filter_query_params)
    return [DataTerm(name=name) for name in terms]


def get_data_sources_types_dp(filter_query_params: FilterQueryParams) -> List[DataSourceType]:
    data_sources = get_distinct_observer_types(filter_query_params)
    return [DataSourceType(name) for name in data_sources]


def get_distinct_languages_dp(filter_query_params: FilterQueryParams) -> List[str]:
    return get_distinct_languages(filter_query_params)


def update_text_analysis_data_dp(tenant_id, text_analysis_update_data: dict) -> int:
    return update_structured_data(tenant_id, text_analysis_update_data)


def get_analysis_data_dp(tenant_id, raw_data_id: int) -> Optional[AnalysisData]:
    filter_query_params = FilterQueryParams(
        tenant_id=tenant_id,
        raw_data_id=raw_data_id
    )
    processed_data_view_list = get_processed_data_view(filter_query_params)
    if not processed_data_view_list or len(processed_data_view_list) > 1:
        return None

    processed_data_view = processed_data_view_list[0]

    return AnalysisData(
        id=processed_data_view.raw_data_id,
        text=processed_data_view.raw_text,
        sentiment=processed_data_view.emotion,
        departments=processed_data_view.taxonomy_tags,
        activities=processed_data_view.taxonomy_terms,
        people=processed_data_view.people,
        source="Google Reviews",
        link=processed_data_view.url,
        rating=processed_data_view.rating,
        timestamp=processed_data_view.event_time.timestamp() if processed_data_view.event_time else None,
        owner_answer_timestamp=None,
        likes=0
    )
