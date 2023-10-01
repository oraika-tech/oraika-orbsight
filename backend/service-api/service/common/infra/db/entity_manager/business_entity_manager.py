from typing import List, Dict, Any
from uuid import UUID

from pydantic import BaseModel
from sqlalchemy import true, func, false
from sqlalchemy.sql import label
from sqlmodel import Session

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
        query = session.query().filter(
            ObserverEntity.is_enabled == true(),
            Entity.is_enabled == true(),
            ObserverEntity.entity_id == Entity.identifier
        )

        query = query.add_columns(
            ObserverEntity.identifier,
            ObserverEntity.type,
            label("url", ObserverEntity.config_data["url"].astext if ObserverEntity.config_data is not None else None),
            label("query", ObserverEntity.config_data["query"].astext if ObserverEntity.config_data is not None else None),
            label("language", ObserverEntity.config_data["language"].astext if ObserverEntity.config_data is not None else None),
            label("country", ObserverEntity.config_data["country"].astext if ObserverEntity.config_data is not None else None),
            label("page_id", ObserverEntity.config_data["page_id"].astext if ObserverEntity.config_data is not None else None),
            label("subreddit", ObserverEntity.config_data["subreddit"].astext if ObserverEntity.config_data is not None else None),
        )

        results = query.limit(200).all()
        return results


def enabled_categories_count(tenant_id: UUID) -> List[EntityCount]:
    with Session(get_tenant_engine(tenant_id)) as session:

        result_set = session.query(
            CategoryEntity.is_enabled,
            func.count(CategoryEntity.is_enabled)
        ).group_by(
            CategoryEntity.is_enabled
        ).filter(
            CategoryEntity.is_deleted == false(),
        ).all()
        total = 0
        tracked = 0
        for flag, count in result_set:
            total += int(count)
            if flag:
                tracked = int(count)

        return [
            EntityCount(name="Tracked", count=tracked),
            EntityCount(name="Total", count=total)
        ]


def enabled_entities_count(tenant_id: UUID) -> List[EntityCount]:
    with Session(get_tenant_engine(tenant_id)) as session:
        result_set = session.query(
            Entity.is_enabled,
            func.count(Entity.is_enabled)
        ).group_by(
            Entity.is_enabled
        ).filter(
            Entity.is_deleted == false(),
        ).all()
        total = 0
        tracked = 0
        for flag, count in result_set:
            total += int(count)
            if flag:
                tracked = int(count)

        return [
            EntityCount(name="Tracked", count=tracked),
            EntityCount(name="Total", count=total)
        ]


def enabled_observers_count(tenant_id: UUID) -> List[EntityCount]:
    with Session(get_tenant_engine(tenant_id)) as session:
        total_count = session.query(
            func.count(ObserverEntity.is_enabled)
        ).filter(
            ObserverEntity.is_deleted == false(),
        ).first()

        total = total_count[0]  # type: ignore

        result_set = session.query(
            func.count(ObserverEntity.is_enabled)
        ).filter(
            ObserverEntity.entity_id == Entity.identifier,
            ObserverEntity.is_enabled == true(),
            Entity.is_enabled == true(),
            Entity.is_deleted == false(),
            ObserverEntity.is_deleted == false(),
        ).all()

        tracked = 0
        for count in result_set:
            tracked += count[0]

        return [
            EntityCount(name="Tracked", count=tracked),
            EntityCount(name="Total", count=total)
        ]


def enabled_taxonomy_count(tenant_id: UUID) -> List[EntityCount]:
    with Session(get_tenant_engine(tenant_id)) as session:

        result_set = session.query(
            TaxonomyEntity.is_enabled,
            func.count(TaxonomyEntity.is_enabled)
        ).group_by(
            TaxonomyEntity.is_enabled
        ).filter(
            TaxonomyEntity.is_deleted == false(),
        ).all()
        total = 0
        tracked = 0
        for flag, count in result_set:
            total += int(count)
            if flag:
                tracked = int(count)

        return [
            EntityCount(name="Tracked", count=tracked),
            EntityCount(name="Total", count=total)
        ]
