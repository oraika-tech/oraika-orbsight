from typing import List, Optional
from uuid import UUID

from sqlalchemy import true, false
from sqlmodel import Field, col, select
from sqlmodel import Session, SQLModel

from service.common.infra.db.db_utils import core_db_engine
from service.common.models import TenantType


class TenantEntity(SQLModel, table=True):
    __tablename__ = "tenant_master"

    identifier: Optional[UUID] = Field(default=None, primary_key=True)

    name: str
    code: str
    type: int
    is_enabled: bool
    is_deleted: bool


def get_tenants(session: Session, tenant_ids: Optional[List[UUID]]) -> List[TenantEntity]:
    if not tenant_ids:
        return []

    return list(session.exec(
        select(TenantEntity).where(
            col(TenantEntity.identifier).in_(tenant_ids),
            TenantEntity.is_enabled == true(),
            TenantEntity.is_deleted == false()
        )
    ).all())


def get_all_enabled_tenants() -> List[TenantEntity]:
    with Session(core_db_engine) as session:
        return list(session.exec(
            select(TenantEntity).where(
                TenantEntity.type == 1,
                TenantEntity.is_enabled == true(),
                TenantEntity.is_deleted == false()
            )
        ).all())


def get_all_demo_tenants() -> List[TenantEntity]:
    with Session(core_db_engine) as session:
        return list(session.exec(
            select(TenantEntity).where(
                TenantEntity.type == TenantType.DEMO,
                TenantEntity.is_enabled == true(),
                TenantEntity.is_deleted == false()
            )
        ).all())


def get_tenant_by_code(tenant_code: str) -> Optional[TenantEntity]:
    with Session(core_db_engine) as session:
        return session.exec(
            select(TenantEntity).where(
                TenantEntity.code == tenant_code,
                TenantEntity.is_enabled == true(),
                TenantEntity.is_deleted == false()
            )
        ).first()


def get_tenant_by_id(tenant_id: UUID) -> Optional[TenantEntity]:
    with Session(core_db_engine) as session:
        return session.exec(
            select(TenantEntity).where(
                TenantEntity.identifier == tenant_id,
                TenantEntity.is_enabled == true(),
                TenantEntity.is_deleted == false()
            )
        ).first()


def get_tenant_by_ids(tenant_ids) -> List[TenantEntity]:
    with Session(core_db_engine) as session:
        tenant_uuids = [tenant_id for tenant_id in tenant_ids]
        return get_tenants(session, tenant_uuids)
