from enum import Enum
from typing import List, Optional
from uuid import UUID

from sqlalchemy import true, false
from sqlmodel import Field as SqlField, col
from sqlmodel import Session, SQLModel

from service.auth.domain.model.domain_models import TenantInfo
from service.common.db.base_entity_manager import BaseEntityManager


class TenantTable(SQLModel, table=True):
    __tablename__ = "tenant_master"

    identifier: Optional[UUID] = SqlField(default=None, primary_key=True)

    name: str
    code: str
    type: int
    is_enabled: bool
    is_deleted: bool


class TenantType(int, Enum):
    DEMO = 0
    CORPORATE = 1
    GOV = 2
    INDIVIDUAL = 3


class TenantEntityManager(BaseEntityManager):

    @staticmethod
    def get_tenants(session: Session, tenant_ids: Optional[List[UUID]]) -> List[TenantInfo]:
        if not tenant_ids:
            return []

        tenants = session.query(TenantTable).filter(
            col(TenantTable.identifier).in_(tenant_ids),
            TenantTable.is_enabled == true(),
            TenantTable.is_deleted == false()
        ).all()

        return [
            TenantInfo(
                identifier=tenant.identifier,
                code=tenant.code,
                name=tenant.name,
            )
            for tenant in tenants
        ]

    def get_all_enabled_tenants(self) -> List[TenantInfo]:
        with Session(self.core_db_engine) as session:
            tenants = session.query(TenantTable).filter(
                TenantTable.type == 1,
                TenantTable.is_enabled == true(),
                TenantTable.is_deleted == false()
            ).all()

            return [
                TenantInfo(
                    identifier=tenant.identifier,
                    code=tenant.code,
                    name=tenant.name
                )
                for tenant in tenants
            ]

    def get_tenant_by_ids(self, tenant_ids) -> List[TenantInfo]:
        with Session(self.core_db_engine) as session:
            tenant_uuids = [UUID(tenant_id) for tenant_id in tenant_ids]
            return self.get_tenants(session, tenant_uuids)

    def get_demo_tenants(self) -> Optional[List[TenantInfo]]:
        with Session(self.core_db_engine) as session:
            tenants = session.query(TenantTable).filter(
                TenantTable.type == TenantType.DEMO,
                TenantTable.is_enabled == true(),
                TenantTable.is_deleted == false()
            )

            if tenants:
                return [
                    TenantInfo(
                        identifier=tenant.identifier,
                        name=tenant.name,
                        code=tenant.code,
                    )
                    for tenant in tenants
                ]
            else:
                return None
