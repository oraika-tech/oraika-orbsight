from abc import abstractmethod
from typing import List, Optional

from pydantic import BaseSettings
from .model.entity import EntityInfo
from .model.stats import StatsInfo
from .model.observer import ObserverInfo
from .model.taxonomy import TaxonomyInfo


class BasePersistenceManager(BaseSettings):

    @abstractmethod
    def get_all_entities(self, company_id: int, enabled: Optional[bool]) -> List[EntityInfo]:
        pass

    @abstractmethod
    def get_entity(self, company_id: int, entity_id: int) -> Optional[EntityInfo]:
        pass

    @abstractmethod
    def enabled_entities_count(self, company_id: int) -> List[StatsInfo]:
        pass

    @abstractmethod
    def entities_type_count(self, company_id: int) -> List[StatsInfo]:
        pass

    @abstractmethod
    def update_entity_enable_state(self, company_id: int, entity_id: int, new_state: bool):
        pass

    # Observer Related API
    @abstractmethod
    def get_all_observers(self, company_id: int, enabled: Optional[bool] = None) -> List[ObserverInfo]:
        pass

    @abstractmethod
    def get_observer(self, company_id: int, observer_id: int) -> Optional[ObserverInfo]:
        pass

    @abstractmethod
    def enabled_observers_count(self, company_id: int) -> List[StatsInfo]:
        pass

    @abstractmethod
    def observer_type_count(self, company_id: int) -> List[StatsInfo]:
        pass

    @abstractmethod
    def update_observer_enable_state(self, company_id: int, observer_id: int, new_state: bool):
        pass

    # Taxonomy Related API
    @abstractmethod
    def get_taxonomy_data(self, company_id: int) -> List[TaxonomyInfo]:
        pass

    @abstractmethod
    def taxonomy_count(self, company_id: int) -> List[StatsInfo]:
        pass

    @abstractmethod
    def get_categories(self, company_id: int) -> List[str]:
        pass

    @abstractmethod
    def categories_count(self, company_id: int) -> List[StatsInfo]:
        pass

    @abstractmethod
    def taxonomy_types_count(self, company_id: int) -> List[StatsInfo]:
        pass
