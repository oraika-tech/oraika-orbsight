from typing import List, Optional
from uuid import UUID

from pydantic import BaseSettings

from .model.category import CategoryInfo
from .model.entity import EntityInfo
from .model.stats import StatsInfo
from .model.observer import ObserverInfo
from .model.taxonomy import TaxonomyInfo
from .base import BasePersistenceManager


class BusinessDomainHandler(BaseSettings):
    persistence_manager: BasePersistenceManager

    def get_all_entities(self, tenant_id: UUID, enabled: Optional[bool]) -> List[EntityInfo]:
        return self.persistence_manager.get_all_entities(tenant_id, enabled)

    def get_entity(self, tenant_id: UUID, entity_id: UUID) -> Optional[EntityInfo]:
        return self.persistence_manager.get_entity(tenant_id, entity_id)

    def enabled_entities_count(self, tenant_id: UUID) -> List[StatsInfo]:
        return self.persistence_manager.enabled_entities_count(tenant_id)

    def update_entity_enable_state(self, tenant_id: UUID, entity_id: UUID, new_state: bool):
        return self.persistence_manager.update_entity_enable_state(tenant_id, entity_id, new_state)

    # Observer Related API
    def get_all_observers(self, tenant_id: UUID, enabled: Optional[bool] = None) -> List[ObserverInfo]:
        return self.persistence_manager.get_all_observers(tenant_id, enabled)

    def get_observer(self, tenant_id: UUID, observer_id: UUID) -> Optional[ObserverInfo]:
        return self.persistence_manager.get_observer(tenant_id, observer_id)

    def enabled_observers_count(self, tenant_id: UUID) -> List[StatsInfo]:
        return self.persistence_manager.enabled_observers_count(tenant_id)

    def update_observer_enable_state(self, tenant_id: UUID, observer_id: UUID, new_state: bool):
        return self.persistence_manager.update_observer_enable_state(tenant_id, observer_id, new_state)

    # Taxonomy Related API
    def get_taxonomy_data(self, tenant_id: UUID) -> List[TaxonomyInfo]:
        return self.persistence_manager.get_taxonomy_data(tenant_id)

    def enabled_taxonomy_count(self, tenant_id: UUID) -> List[StatsInfo]:
        return self.persistence_manager.enabled_taxonomy_count(tenant_id)

    def get_categories(self, tenant_id: UUID) -> List[CategoryInfo]:
        return self.persistence_manager.get_categories(tenant_id)

    def enabled_categories_count(self, tenant_id: UUID) -> List[StatsInfo]:
        return self.persistence_manager.enabled_categories_count(tenant_id)
