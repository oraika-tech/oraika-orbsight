from typing import List, Optional

from pydantic import BaseSettings
from .model.entity import EntityInfo
from .model.stats import StatsInfo
from .model.observer import ObserverInfo
from .model.taxonomy import TaxonomyInfo
from .base import BasePersistenceManager


class BusinessDomainHandler(BaseSettings):
    persistence_manager: BasePersistenceManager

    def get_all_entities(self, company_id: int, enabled: Optional[bool]) -> List[EntityInfo]:
        return self.persistence_manager.get_all_entities(company_id, enabled)

    def get_entity(self, company_id: int, entity_id: int) -> Optional[EntityInfo]:
        return self.persistence_manager.get_entity(company_id, entity_id)

    def enabled_entities_count(self, company_id: int) -> List[StatsInfo]:
        return self.persistence_manager.enabled_entities_count(company_id)

    def entities_type_count(self, company_id: int) -> List[StatsInfo]:
        return self.persistence_manager.entities_type_count(company_id)

    def update_entity_enable_state(self, company_id: int, entity_id: int, new_state: bool):
        return self.persistence_manager.update_entity_enable_state(company_id, entity_id, new_state)

    # Observer Related API
    def get_all_observers(self, company_id: int, enabled: Optional[bool] = None) -> List[ObserverInfo]:
        return self.persistence_manager.get_all_observers(company_id, enabled)

    def get_observer(self, company_id: int, observer_id: int) -> Optional[ObserverInfo]:
        return self.persistence_manager.get_observer(company_id, observer_id)

    def enabled_observers_count(self, company_id: int) -> List[StatsInfo]:
        return self.persistence_manager.enabled_observers_count(company_id)

    def observer_type_count(self, company_id: int) -> List[StatsInfo]:
        return self.persistence_manager.observer_type_count(company_id)

    def update_observer_enable_state(self, company_id: int, observer_id: int, new_state: bool):
        return self.persistence_manager.update_observer_enable_state(company_id, observer_id, new_state)

    # Taxonomy Related API
    def get_taxonomy_data(self, company_id: int) -> List[TaxonomyInfo]:
        return self.persistence_manager.get_taxonomy_data(company_id)

    def taxonomy_count(self, company_id: int) -> List[StatsInfo]:
        return self.persistence_manager.taxonomy_count(company_id)

    def get_categories(self, company_id: int) -> List[str]:
        return self.persistence_manager.get_categories(company_id)

    def categories_count(self, company_id: int) -> List[StatsInfo]:
        return self.persistence_manager.categories_count(company_id)

    def taxonomy_types_count(self, company_id: int) -> List[StatsInfo]:
        return self.persistence_manager.taxonomy_types_count(company_id)
