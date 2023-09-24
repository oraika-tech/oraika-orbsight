from typing import List
from uuid import UUID

from cachetools import TTLCache, cached
from pandas import DataFrame
from sqlalchemy import true, false
from sqlmodel import Session

from service.business.persistence.db_manager import TaxonomyEntity, CategoryEntity
from service.common.db.base_entity_manager import BaseEntityManager
from service.common.db.cache_settings import cache_settings


class TaxonomyEntityManager(BaseEntityManager):

    def hash_key(self, tenant_id: UUID):
        return tenant_id

    # Keeping it to less than equal to cron period. Main idea that at least it can handle single burst of events
    @cached(cache=TTLCache(maxsize=cache_settings.CACHE_MAX_SIZE, ttl=cache_settings.CACHE_TTL), key=hash_key)
    def get_taxonomy_dataframe(self, tenant_id: UUID) -> DataFrame:
        with Session(self._get_tenant_engine(tenant_id)) as session:
            taxonomy_entities = session.query(TaxonomyEntity).filter(
                TaxonomyEntity.is_deleted == false(),
                TaxonomyEntity.is_enabled == true(),
            )
            if taxonomy_entities:
                return DataFrame(
                    [taxonomy_entity.as_dict() for taxonomy_entity in taxonomy_entities]
                ).convert_dtypes().apply(lambda col: col.str.lower())
                # todo: Need to apply lower only on keyword column

            return DataFrame()

    @cached(cache=TTLCache(maxsize=cache_settings.CACHE_MAX_SIZE, ttl=cache_settings.CACHE_TTL), key=hash_key)
    def get_categories(self, tenant_id: UUID) -> List[str]:
        with Session(self._get_tenant_engine(tenant_id)) as session:
            category_entities = session.query(CategoryEntity).filter(
                CategoryEntity.is_deleted == false(),
                CategoryEntity.is_enabled == true(),
            )
            if category_entities:
                return [category_entity.name for category_entity in category_entities]
            return []
