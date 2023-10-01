from typing import List, Optional
from uuid import UUID

from service.app.business import business_db_provider as db_provider
from service.app.business.business_db_provider import get_all_entities_dp
from service.app.business.business_models import ObserverInfo, CategoryInfo, EntityInfo, StatsInfo, TaxonomyInfo


def get_all_entities(tenant_id: UUID, enabled: Optional[bool]) -> List[EntityInfo]:
    return get_all_entities_dp(tenant_id, enabled)


def get_entity(tenant_id: UUID, entity_id: UUID) -> Optional[EntityInfo]:
    return db_provider.get_entity(tenant_id, entity_id)


def enabled_entities_count(tenant_id: UUID) -> List[StatsInfo]:
    return db_provider.enabled_entities_count_dp(tenant_id)


def update_entity_enable_state(tenant_id: UUID, entity_id: UUID, new_state: bool):
    return db_provider.update_entity_enable_state(tenant_id, entity_id, new_state)


# ObserverEntity Related API
def get_all_observers(tenant_id: UUID, enabled: Optional[bool] = None) -> List[ObserverInfo]:
    return db_provider.get_all_observers_dp(tenant_id, enabled)


def get_observer(tenant_id: UUID, observer_id: UUID) -> Optional[ObserverInfo]:
    return db_provider.get_observer(tenant_id, observer_id)


def enabled_observers_count(tenant_id: UUID) -> List[StatsInfo]:
    return db_provider.enabled_observers_count_dp(tenant_id)


def update_observer_enable_state(tenant_id: UUID, observer_id: UUID, new_state: bool):
    return db_provider.update_observer_enable_state(tenant_id, observer_id, new_state)


# Taxonomy Related API
def get_taxonomy_data(tenant_id: UUID) -> List[TaxonomyInfo]:
    return db_provider.get_taxonomy_data(tenant_id)


def enabled_taxonomy_count(tenant_id: UUID) -> List[StatsInfo]:
    return db_provider.enabled_taxonomy_count_dp(tenant_id)


def get_categories(tenant_id: UUID) -> List[CategoryInfo]:
    return db_provider.get_categories(tenant_id)


def enabled_categories_count(tenant_id: UUID) -> List[StatsInfo]:
    return db_provider.enabled_categories_count_dp(tenant_id)
