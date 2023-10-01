from typing import Optional, List
from uuid import UUID

from sqlalchemy import false
from sqlmodel import SQLModel, Field as SqlField, Session, col

from service.common.infra.db.db_utils import get_tenant_engine


class Entity(SQLModel, table=True):
    __tablename__ = "config_entity"

    identifier: Optional[UUID] = SqlField(default=None, primary_key=True)
    name: str
    tags: Optional[List[str]]
    is_enabled: bool
    is_deleted: bool


def get_all_entities(tenant_id: UUID, enabled: Optional[bool] = None) -> List[Entity]:
    with Session(get_tenant_engine(tenant_id)) as session:
        query = session.query(Entity).filter(
            Entity.is_deleted == false()
        ).order_by(
            col(Entity.is_enabled).desc(),
            Entity.name
        )
        if enabled is not None:
            query = query.filter(
                Entity.is_enabled == enabled
            )

        return query.all()


def get_entity_by_id(tenant_id: UUID, entity_id: UUID) -> Optional[Entity]:
    with Session(get_tenant_engine(tenant_id)) as session:
        return session.query(Entity).filter(
            Entity.identifier == entity_id,
            Entity.is_deleted == false(),
        ).first()


def update_entity_enable_state(tenant_id: UUID, entity_id: UUID, new_state: bool):
    with Session(get_tenant_engine(tenant_id)) as session:
        session.query(Entity).filter(
            Entity.identifier == entity_id,
            Entity.is_deleted == false(),
        ).update(
            {'is_enabled': new_state}
        )
        session.commit()
