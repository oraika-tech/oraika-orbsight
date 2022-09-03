from typing import List, Set

from cachetools import TTLCache, cached
from pydantic import BaseSettings
from service.common.settings import settings
from service.data.domain.model.term import DataTerm

from .base import BasePersistenceManager
from .key_phrases_handler import KeyPhrasesHandler
from .model.entity import DataEntity
from .model.filter_query_params import FilterQueryParams
from .model.source_type import DataSourceType
from .model.text_analysis_data import TextAnalysisData
from .word_freq_handler import WordFreqHandler

LANG_CODE_TO_NAME = {
    "en": "English",
    "hi": "Hindi",
    "ta": "Tamil",
    "te": "Telugu",
    "gu": "Gujarati",
    "kn": "Kannada",
    "bn": "Bengali",
    "mr": "Marathi",
    "ml": "Malayalam",
    "pa": "Punjabi",
    "ur": "Urdu"
}


class DataDomainHandler(BaseSettings):
    persistence_manager: BasePersistenceManager
    word_freq_handler: WordFreqHandler
    key_phrases_handler: KeyPhrasesHandler

    def hash_key(self, filter_query_params: FilterQueryParams):
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

    def get_text_analysis_data(self, filter_query_params: FilterQueryParams) -> List[TextAnalysisData]:
        if not filter_query_params.limit:
            filter_query_params.limit = settings.DEFAULT_QUERY_LIMIT
        return self.persistence_manager.get_text_analysis_data(filter_query_params)

    @cached(cache=TTLCache(maxsize=settings.CACHE_MAX_SIZE, ttl=settings.CACHE_TTL), key=hash_key)
    def get_data_entities(self, filter_query_params: FilterQueryParams):
        entity_names = self.persistence_manager.get_distinct_entity_names(filter_query_params)
        return [DataEntity(name=name) for name in entity_names]

    @cached(cache=TTLCache(maxsize=settings.CACHE_MAX_SIZE, ttl=settings.CACHE_TTL), key=hash_key)
    def get_data_terms(self, filter_query_params: FilterQueryParams):
        terms = self.persistence_manager.get_distinct_terms(filter_query_params)
        return [DataTerm(name=name) for name in terms]

    @cached(cache=TTLCache(maxsize=settings.CACHE_MAX_SIZE, ttl=settings.CACHE_TTL), key=hash_key)
    def get_data_sources_types(self, filter_query_params: FilterQueryParams):
        data_sources = self.persistence_manager.get_distinct_observer_types(filter_query_params)
        return [DataSourceType(name=name) for name in data_sources]

    @cached(cache=TTLCache(maxsize=settings.CACHE_MAX_SIZE, ttl=settings.CACHE_TTL), key=hash_key)
    def get_languages(self, filter_query_params: FilterQueryParams):
        language_codes: Set[str] = set(self.persistence_manager.get_distinct_languages(filter_query_params))
        return [code for code in LANG_CODE_TO_NAME if code in language_codes]

    @cached(cache=TTLCache(maxsize=settings.CACHE_MAX_SIZE, ttl=settings.CACHE_TTL), key=hash_key)
    def get_word_cloud(self, filter_query_params: FilterQueryParams):
        data = self.get_text_analysis_data(filter_query_params)
        return self.word_freq_handler.generate_word_freq(data=data, lang_code=filter_query_params.lang_code)

    @cached(cache=TTLCache(maxsize=settings.CACHE_MAX_SIZE, ttl=settings.CACHE_TTL), key=hash_key)
    def get_key_phrases(self, filter_query_params: FilterQueryParams):
        data = self.get_text_analysis_data(filter_query_params)
        return self.key_phrases_handler.generate_key_phrases(data=data, lang_code=filter_query_params.lang_code)
