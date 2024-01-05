from typing import List, Dict, Any
from uuid import UUID

from pydantic import BaseModel
from sqlalchemy import true, func, false, literal_column, Boolean
from sqlmodel import Session, select, cast

from service.common.infra.db.db_utils import get_tenant_engine
from service.common.infra.db.repository.business.category_repository import CategoryEntity
from service.common.infra.db.repository.business.entity_repository import Entity
from service.common.infra.db.repository.business.observer_repository import ObserverEntity
from service.common.infra.db.repository.business.taxonomy_repository import TaxonomyEntity


class EntityCount(BaseModel):
    name: str
    count: int


def get_observer_tasks(tenant_id: UUID) -> List[Dict[Any, Any]]:
    with Session(get_tenant_engine(tenant_id)) as session:
        query = select(ObserverEntity, Entity).where(
            ObserverEntity.is_enabled == true(),
            Entity.is_enabled == true(),
            ObserverEntity.is_deleted == false(),
            Entity.is_deleted == false(),
            ObserverEntity.entity_id == Entity.identifier
        )
        results = session.exec(query.limit(200)).all()

        return [
            {
                "identifier": observer.identifier,
                "type": observer.type,
                "url": (observer.config_data.get("url") if observer.config_data is not None else None),
                "query": (observer.config_data.get("query") if observer.config_data is not None else None),
                "language": (observer.config_data.get("language") if observer.config_data is not None else None),
                "country": (observer.config_data.get("country") if observer.config_data is not None else None),
                "page_id": (observer.config_data.get("page_id") if observer.config_data is not None else None),
                "subreddit": (observer.config_data.get("subreddit") if observer.config_data is not None else None)
            }
            for observer, entity in results
        ]


def enabled_categories_count(tenant_id: UUID) -> List[EntityCount]:
    with Session(get_tenant_engine(tenant_id)) as session:
        total: int = session.exec(
            select(func.count(literal_column('*')))
            .where(CategoryEntity.is_deleted == false())
        ).one()

        tracked: int = session.exec(
            select(func.count(literal_column('*')))
            .where(CategoryEntity.is_deleted == false(), CategoryEntity.is_enabled == true())
        ).one()

        return [
            EntityCount(name="Tracked", count=tracked),
            EntityCount(name="Total", count=total)
        ]


def enabled_entities_count(tenant_id: UUID) -> List[EntityCount]:
    with Session(get_tenant_engine(tenant_id)) as session:
        total: int = session.exec(
            select(func.count(literal_column('*')))
            .where(Entity.is_deleted == false())
        ).one()

        tracked: int = session.exec(
            select(func.count(literal_column('*')))
            .where(Entity.is_deleted == false(), Entity.is_enabled == true())
        ).one()

        return [
            EntityCount(name="Tracked", count=tracked),
            EntityCount(name="Total", count=total)
        ]


def enabled_observers_count(tenant_id: UUID) -> List[EntityCount]:
    with Session(get_tenant_engine(tenant_id)) as session:
        total: int = session.exec(
            select(func.count(literal_column('*')))
            .where(ObserverEntity.is_deleted == false())
        ).one()

        tracked: int = session.exec(
            select(func.count(literal_column('*')))
            .select_from(ObserverEntity)
            .join(Entity, onclause=cast(ObserverEntity.entity_id == Entity.identifier, Boolean))
            .where(
                ObserverEntity.is_deleted == false(),
                ObserverEntity.is_enabled == true(),
                Entity.is_enabled == true(),
                Entity.is_deleted == false()
            )
        ).one()

        return [
            EntityCount(name="Tracked", count=tracked),
            EntityCount(name="Total", count=total)
        ]


def enabled_taxonomy_count(tenant_id: UUID) -> List[EntityCount]:
    with Session(get_tenant_engine(tenant_id)) as session:
        total: int = session.exec(
            select(func.count(literal_column('*')))
            .where(TaxonomyEntity.is_deleted == false())
        ).one()

        tracked: int = session.exec(
            select(func.count(literal_column('*')))
            .where(TaxonomyEntity.is_deleted == false(), TaxonomyEntity.is_enabled == true())
        ).one()

        return [
            EntityCount(name="Tracked", count=tracked),
            EntityCount(name="Total", count=total)
        ]
