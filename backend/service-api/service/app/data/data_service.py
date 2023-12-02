from typing import List, Set
from uuid import UUID

from cachetools import TTLCache, cached

from service.app.data import data_db_provider as db_provider
from service.app.data.data_models import TextAnalysisData, LANG_CODE_TO_NAME, DataEntity, DataTerm
from service.app.data.utils.key_phrases_utils import generate_key_phrases
from service.app.data.utils.word_freq_utils import generate_word_freq
from service.common.config.app_settings import app_settings
from service.common.models import DataSourceType, FilterQueryParams


def hash_key(filter_query_params: FilterQueryParams):
    return (
        filter_query_params.tenant_id,
        filter_query_params.start_date,
        filter_query_params.end_date,
        filter_query_params.entity_name,
        filter_query_params.term,
        filter_query_params.lang_code,
        filter_query_params.observer_type,
        filter_query_params.emotion,
        filter_query_params.limit
    )


def get_text_analysis_data(filter_query_params: FilterQueryParams) -> List[TextAnalysisData]:
    if not filter_query_params.limit:
        filter_query_params.limit = app_settings.DEFAULT_QUERY_LIMIT
    return db_provider.get_text_analysis_data_dp(filter_query_params)


@cached(cache=TTLCache(maxsize=app_settings.CACHE_MAX_SIZE, ttl=app_settings.CACHE_TTL), key=hash_key)
def get_data_entities(filter_query_params: FilterQueryParams) -> List[DataEntity]:
    return db_provider.get_data_entities_dp(filter_query_params)


@cached(cache=TTLCache(maxsize=app_settings.CACHE_MAX_SIZE, ttl=app_settings.CACHE_TTL), key=hash_key)
def get_data_terms(filter_query_params: FilterQueryParams) -> List[DataTerm]:
    return db_provider.get_data_terms_dp(filter_query_params)


@cached(cache=TTLCache(maxsize=app_settings.CACHE_MAX_SIZE, ttl=app_settings.CACHE_TTL), key=hash_key)
def get_data_sources_types(filter_query_params: FilterQueryParams) -> List[DataSourceType]:
    return db_provider.get_data_sources_types_dp(filter_query_params)


@cached(cache=TTLCache(maxsize=app_settings.CACHE_MAX_SIZE, ttl=app_settings.CACHE_TTL), key=hash_key)
def get_languages(filter_query_params: FilterQueryParams):
    language_codes: Set[str] = set(db_provider.get_distinct_languages(filter_query_params))
    return [code for code in LANG_CODE_TO_NAME if code in language_codes]


@cached(cache=TTLCache(maxsize=app_settings.CACHE_MAX_SIZE, ttl=app_settings.CACHE_TTL), key=hash_key)
def get_word_cloud(filter_query_params: FilterQueryParams):
    data = db_provider.get_text_analysis_data_dp(filter_query_params)
    return generate_word_freq(data=data, lang_code=filter_query_params.lang_code or 'en') if data else []


@cached(cache=TTLCache(maxsize=app_settings.CACHE_MAX_SIZE, ttl=app_settings.CACHE_TTL), key=hash_key)
def get_key_phrases(filter_query_params: FilterQueryParams):
    data = db_provider.get_text_analysis_data_dp(filter_query_params)
    return generate_key_phrases(data=data) if data else []


def update_text_analysis_data(tenant_id: UUID, text_analysis_update_data: dict) -> int:
    return db_provider.update_text_analysis_data_dp(tenant_id, text_analysis_update_data)


def get_analysis_data(tenant_id: UUID, raw_data_id: int):
    return db_provider.get_analysis_data_dp(tenant_id, raw_data_id)
