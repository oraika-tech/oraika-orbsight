from typing import Optional, List
from uuid import UUID

from sqlalchemy import Column, Text, true, false
from sqlalchemy.dialects.postgresql import ARRAY, JSONB
from sqlmodel import SQLModel, Field as SqlField, Session, col

from service.common.infra.db.db_utils import get_tenant_engine
from service.common.models import ComponentLayoutDO


class DashboardEntity(SQLModel, table=True):
    __tablename__ = "viz_dashboard"

    identifier: Optional[UUID] = SqlField(default=None, primary_key=True)
    frontend_keys: List[str] = SqlField(default='{}', sa_column=Column(ARRAY(Text)))
    title: str
    component_layout: ComponentLayoutDO = SqlField(default='{}', sa_column=Column(JSONB))

    is_enabled: bool
    is_deleted: bool


def get_dashboard(tenant_id: UUID, dashboard_id: UUID) -> Optional[DashboardEntity]:
    with Session(get_tenant_engine(tenant_id)) as session:
        return session.query(DashboardEntity).filter(
            DashboardEntity.identifier == dashboard_id,
            DashboardEntity.is_enabled == true(),
            DashboardEntity.is_deleted == false()
        ).first()


def get_dashboards(tenant_id: UUID, frontend_key: str) -> List[DashboardEntity]:
    with Session(get_tenant_engine(tenant_id)) as session:
        query = session.query(DashboardEntity).filter(
            DashboardEntity.is_enabled == true(),
            DashboardEntity.is_deleted == false()
        )
        if frontend_key:
            query = query.filter(
                col(DashboardEntity.frontend_keys).any(frontend_key)
            )
        return query.all()
