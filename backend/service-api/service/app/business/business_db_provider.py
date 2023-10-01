from typing import List, Optional
from uuid import UUID

from cachetools import cached, TTLCache
from pandas import DataFrame

from service.app.business.business_models import EntityInfo, StatsInfo, ObserverInfo, TaxonomyInfo, CategoryInfo
from service.app.data.data_models import RawData
from service.common.config.cache_settings import cache_settings
from service.common.infra.db.entity_manager.business_entity_manager import (enabled_entities_count, enabled_observers_count,
                                                                            enabled_categories_count, enabled_taxonomy_count)
from service.common.infra.db.repository.business.category_repository import get_all_category
from service.common.infra.db.repository.business.entity_repository import get_all_entities, get_entity_by_id, update_entity_enable_state
from service.common.infra.db.repository.business.observer_repository import get_all_observers, get_observer_by_id, update_observer_enable_state
from service.common.infra.db.repository.business.taxonomy_repository import get_taxonomies
from service.common.infra.db.repository.data.raw_data_repository import RawDataEntity, insert_raw_data
from service.common.utils.reflection_utils import convert_models, convert_model


def hash_key(tenant_id: UUID):
    return tenant_id


def get_all_entities_dp(tenant_id: UUID, enabled: Optional[bool]) -> List[EntityInfo]:
    return [
        EntityInfo(
            identifier=entity.identifier,
            name=entity.name,
            tags=entity.tags,
            is_enabled=entity.is_enabled
        )
        for entity in get_all_entities(tenant_id, enabled)
    ]


def get_entity(tenant_id: UUID, entity_id: UUID) -> Optional[EntityInfo]:
    entity = get_entity_by_id(tenant_id, entity_id)
    if not entity:
        return None

    return EntityInfo(
        identifier=entity.identifier,
        name=entity.name,
        tags=entity.tags,
        is_enabled=entity.is_enabled
    )


def enabled_entities_count_dp(tenant_id: UUID) -> List[StatsInfo]:
    stats = enabled_entities_count(tenant_id)
    return [StatsInfo(name=stat.name, value=stat.count) for stat in stats]


def update_entity_enable_state_dp(tenant_id: UUID, entity_id: UUID, new_state: bool):
    return update_entity_enable_state(tenant_id, entity_id, new_state)


# ObserverEntity Related API
def get_all_observers_dp(tenant_id: UUID, enabled: Optional[bool] = None) -> List[ObserverInfo]:
    observers = get_all_observers(tenant_id, enabled)
    entities = get_all_entities(tenant_id)
    observers_info: List[ObserverInfo] = []
    for observer in observers:
        entity_name = ''
        for entity in entities:
            if observer.entity_id == entity.identifier:
                entity_name = entity.name
        observers_info.append(ObserverInfo(
            identifier=observer.identifier,
            name=observer.name,
            type=observer.type,
            entity_id=observer.entity_id,
            entity_name=entity_name,
            config_data=observer.config_data,
            is_enabled=observer.is_enabled
        ))
    return observers_info


def get_observer(tenant_id: UUID, observer_id: UUID) -> Optional[ObserverInfo]:
    observer = get_observer_by_id(tenant_id, observer_id)
    return convert_model(observer, ObserverInfo)


def enabled_observers_count_dp(tenant_id: UUID) -> List[StatsInfo]:
    stats = enabled_observers_count(tenant_id)
    return [StatsInfo(name=stat.name, value=stat.count) for stat in stats]


def update_observer_enable_state_dp(tenant_id: UUID, observer_id: UUID, new_state: bool):
    return update_observer_enable_state(tenant_id, observer_id, new_state)


def get_categories(tenant_id: UUID) -> List[CategoryInfo]:
    categories = get_all_category(tenant_id)
    return convert_models(categories, CategoryInfo)


def enabled_categories_count_dp(tenant_id: UUID) -> List[StatsInfo]:
    stats = enabled_categories_count(tenant_id)
    return [StatsInfo(name=stat.name, value=stat.count) for stat in stats]


def enabled_taxonomy_count_dp(tenant_id: UUID) -> List[StatsInfo]:
    stats = enabled_taxonomy_count(tenant_id)
    return [StatsInfo(name=stat.name, value=stat.count) for stat in stats]


def get_taxonomy_data(tenant_id: UUID) -> List[TaxonomyInfo]:
    taxonomies = get_taxonomies(tenant_id)
    return convert_models(taxonomies, TaxonomyInfo)


@cached(cache=TTLCache(maxsize=cache_settings.CACHE_MAX_SIZE, ttl=cache_settings.CACHE_TTL), key=hash_key)
def get_taxonomy_dataframe(tenant_id: UUID) -> DataFrame:
    taxonomy_entities = get_taxonomies(tenant_id)
    if taxonomy_entities:
        return DataFrame(
            [taxonomy_entity.dict() for taxonomy_entity in taxonomy_entities]
        ).convert_dtypes().apply(lambda col: col.str.lower())
        # todo: Need to apply lower only on keyword column
    else:
        return DataFrame()


@cached(cache=TTLCache(maxsize=cache_settings.CACHE_MAX_SIZE, ttl=cache_settings.CACHE_TTL), key=hash_key)
def get_category_names(tenant_id: UUID) -> List[str]:
    category_entities = get_categories(tenant_id)
    if category_entities:
        return [category_entity.name for category_entity in category_entities]
    else:
        return []


def insert_raw_data_dp(tenant_id: UUID, raw_data_list: List[RawData]) -> List[RawData]:
    if not raw_data_list:
        return []
    raw_data_entities = convert_models(raw_data_list, RawDataEntity)
    inserted_entities = insert_raw_data(tenant_id, raw_data_entities)
    return convert_models(inserted_entities, RawData)
