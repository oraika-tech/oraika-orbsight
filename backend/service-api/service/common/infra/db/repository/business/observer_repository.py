from typing import Optional, List
from uuid import UUID

from sqlalchemy import Column, false
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import SQLModel, Field as SqlField, Session, col

from service.common.infra.db.db_utils import get_tenant_engine


class ObserverEntity(SQLModel, table=True):
    __tablename__ = "config_observer"

    identifier: Optional[UUID] = SqlField(default=None, primary_key=True)
    name: str
    type: int
    entity_id: UUID
    config_data: dict = SqlField(default='{}', sa_column=Column(JSONB))
    is_enabled: bool
    is_deleted: bool


def get_all_observers(tenant_id: UUID, enabled: Optional[bool] = None) -> List[ObserverEntity]:
    with Session(get_tenant_engine(tenant_id)) as session:
        query = session.query(ObserverEntity).filter(
            ObserverEntity.is_deleted == false(),
        ).order_by(
            col(ObserverEntity.is_enabled).desc(),
            ObserverEntity.entity_id,
            ObserverEntity.name
        )
        if enabled is not None:
            query = query.filter(
                ObserverEntity.is_enabled == enabled
            )
        return query.all()


def get_observer_by_id(tenant_id: UUID, observer_id: UUID) -> Optional[ObserverEntity]:
    with Session(get_tenant_engine(tenant_id)) as session:
        return session.query(ObserverEntity).filter(
            ObserverEntity.identifier == observer_id,
            ObserverEntity.is_deleted == false()
        ).first()


def update_observer_enable_state(tenant_id: UUID, observer_id: UUID, new_state: bool):
    with Session(get_tenant_engine(tenant_id)) as session:
        session.query(ObserverEntity).filter(
            ObserverEntity.identifier == observer_id,
            ObserverEntity.is_deleted == false(),
        ).update(
            {'is_enabled': new_state}
        )
        session.commit()
