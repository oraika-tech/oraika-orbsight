import json
from abc import abstractmethod
from typing import List, Optional

from pydantic import BaseSettings

from .model.filter_query_params import FilterQueryParams
from .model.text_analysis_data import TextAnalysisData


class BasePersistenceManager(BaseSettings):

    @abstractmethod
    def get_text_analysis_data(self, params: FilterQueryParams) -> Optional[List[TextAnalysisData]]:
        pass

    @abstractmethod
    def get_distinct_entity_names(self, params: FilterQueryParams) -> Optional[List[str]]:
        pass

    @abstractmethod
    def get_distinct_terms(self, params: FilterQueryParams) -> Optional[List[str]]:
        pass

    @abstractmethod
    def get_distinct_observer_types(self, params: FilterQueryParams) -> Optional[List[str]]:
        pass

    @abstractmethod
    def get_distinct_languages(self, params: FilterQueryParams) -> Optional[List[str]]:
        pass
