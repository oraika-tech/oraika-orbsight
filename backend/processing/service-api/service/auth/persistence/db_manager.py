from enum import Enum
from typing import List, Optional
from uuid import UUID

import bcrypt
from sqlalchemy import Column, true, false
from sqlalchemy.dialects.postgresql import ARRAY, UUID as DB_UUID
from sqlmodel import Field as SqlField, col
from sqlmodel import Session, SQLModel

from service.auth.domain.base import BasePersistenceManager
from service.auth.domain.model.domain_models import TenantInfo
from service.common.base_entity_manager import BaseEntityManager
from service.common.model.user import UserInfo


class UserTable(SQLModel, table=True):
    __tablename__ = "user_master"

    identifier: Optional[UUID] = SqlField(default=None, primary_key=True)
    tenant_ids: List[UUID] = SqlField(sa_column=Column(ARRAY(DB_UUID)))
    name: str
    email: str
    hash_password: str
    is_enabled: bool
    is_deleted: bool


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


class UserDBManager(BasePersistenceManager, BaseEntityManager):

    def verify_user(self, email: str, password: str) -> Optional[UserInfo]:
        with Session(self.core_db_engine) as session:
            user_entity = session.query(UserTable).filter(
                UserTable.is_deleted == false(),
                UserTable.is_enabled == true(),
                UserTable.email == email
            ).first()

            if user_entity:
                tenants = self.get_tenants(session, user_entity.tenant_ids)
                if bcrypt.checkpw(password.encode(), user_entity.hash_password.encode()):
                    return UserInfo(
                        identifier=str(user_entity.identifier),
                        tenants=tenants,
                        name=user_entity.name,
                        email=user_entity.email
                    )

        return None

    def get_user(self, user_id: str) -> Optional[UserInfo]:
        with Session(self.core_db_engine) as session:
            user_entity = session.query(UserTable).filter(
                UserTable.identifier == user_id,
                UserTable.is_enabled == true(),
                UserTable.is_deleted == false()
            ).first()

            if user_entity:
                tenants = self.get_tenants(session, user_entity.tenant_ids)
                return UserInfo(
                    identifier=user_entity.identifier,
                    tenants=tenants,
                    name=user_entity.name,
                    email=user_entity.email
                )
        return None

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
