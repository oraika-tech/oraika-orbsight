from typing import Optional, List
from uuid import UUID

from sqlalchemy import Column, Text, true, false
from sqlalchemy.dialects.postgresql import ARRAY, JSONB
from sqlmodel import SQLModel, Field, Session, select, any_

from service.common.infra.db.db_utils import get_tenant_engine
from service.common.models import ComponentLayoutDO


class DashboardEntity(SQLModel, table=True):
    __tablename__ = "viz_dashboard"

    identifier: Optional[UUID] = Field(default=None, primary_key=True)
    frontend_keys: List[str] = Field(default='{}', sa_column=Column(ARRAY(Text)))
    title: str
    component_layout: ComponentLayoutDO = Field(default='{}', sa_column=Column(JSONB))

    is_enabled: bool
    is_deleted: bool


def get_dashboard(tenant_id: UUID, dashboard_id: UUID) -> Optional[DashboardEntity]:
    with Session(get_tenant_engine(tenant_id)) as session:
        return session.exec(
            select(DashboardEntity).where(
                DashboardEntity.identifier == dashboard_id,
                DashboardEntity.is_enabled == true(),
                DashboardEntity.is_deleted == false()
            )
        ).first()


def get_dashboards(tenant_id: UUID, frontend_key: str) -> List[DashboardEntity]:
    with Session(get_tenant_engine(tenant_id)) as session:
        query = select(DashboardEntity).where(
            DashboardEntity.is_enabled == true(),
            DashboardEntity.is_deleted == false()
        )

        if frontend_key:
            query = query.where(
                any_(DashboardEntity.frontend_keys) == frontend_key
            )
        return list(session.exec(query).all())

