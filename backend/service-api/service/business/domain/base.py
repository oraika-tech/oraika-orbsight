from abc import abstractmethod
from typing import List, Optional
from uuid import UUID

from pydantic import BaseSettings

from .model.category import CategoryInfo
from .model.entity import EntityInfo
from .model.observer import ObserverInfo
from .model.stats import StatsInfo
from .model.taxonomy import TaxonomyInfo


class BasePersistenceManager(BaseSettings):

    @abstractmethod
    def get_all_entities(self, tenant_id: UUID, enabled: Optional[bool]) -> List[EntityInfo]:
        pass

    @abstractmethod
    def get_entity(self, tenant_id: UUID, entity_id: UUID) -> Optional[EntityInfo]:
        pass

    @abstractmethod
    def enabled_entities_count(self, tenant_id: UUID) -> List[StatsInfo]:
        pass

    @abstractmethod
    def update_entity_enable_state(self, tenant_id: UUID, entity_id: UUID, new_state: bool):
        pass

    # Observer Related API
    @abstractmethod
    def get_all_observers(self, tenant_id: UUID, enabled: Optional[bool] = None) -> List[ObserverInfo]:
        pass

    @abstractmethod
    def get_observer(self, tenant_id: UUID, observer_id: UUID) -> Optional[ObserverInfo]:
        pass

    @abstractmethod
    def enabled_observers_count(self, tenant_id: UUID) -> List[StatsInfo]:
        pass

    @abstractmethod
    def update_observer_enable_state(self, tenant_id: UUID, observer_id: UUID, new_state: bool):
        pass

    # Taxonomy Related API
    @abstractmethod
    def get_taxonomy_data(self, tenant_id: UUID) -> List[TaxonomyInfo]:
        pass

    @abstractmethod
    def enabled_taxonomy_count(self, tenant_id: UUID) -> List[StatsInfo]:
        pass

    @abstractmethod
    def get_categories(self, tenant_id: UUID) -> List[CategoryInfo]:
        pass

    @abstractmethod
    def enabled_categories_count(self, tenant_id: UUID) -> List[StatsInfo]:
        pass

    @abstractmethod
    def get_dashboards(self, tenant_id: UUID) -> List[dict]:
        pass

    @abstractmethod
    def get_panels(self, tenant_id: UUID) -> Optional[dict]:
        pass
