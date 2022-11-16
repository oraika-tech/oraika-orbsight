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
    nile_org_id: str
    is_enabled: bool
    is_deleted: bool


class UserDBManager(BasePersistenceManager, BaseEntityManager):

    def verify_user(self, email: str, password: str) -> Optional[UserInfo]:
        with Session(self.core_db_engine) as session:
            user_entity = session.query(UserTable).filter(
                UserTable.is_deleted == false(),
                UserTable.is_enabled == true(),
                UserTable.email == email
            ).first()

            tenant_codes = self.get_tenant_codes(session, user_entity.tenant_ids)

            if user_entity is not None:
                if bcrypt.checkpw(password.encode(), user_entity.hash_password.encode()):
                    return UserInfo(
                        identifier=user_entity.identifier,
                        tenant_ids=user_entity.tenant_ids,
                        tenant_codes=tenant_codes,
                        name=user_entity.name,
                        email=user_entity.email
                    )

    def get_user(self, user_id: str) -> Optional[UserInfo]:
        with Session(self.core_db_engine) as session:
            user_entity = session.query(UserTable).filter(
                UserTable.identifier == user_id,
                UserTable.is_enabled == true(),
                UserTable.is_deleted == false()
            ).first()

            tenant_codes = self.get_tenant_codes(session, user_entity.tenant_ids)

            if user_entity is not None:
                return UserInfo(
                    identifier=user_entity.identifier,
                    tenant_ids=user_entity.tenant_ids,
                    tenant_codes=tenant_codes,
                    name=user_entity.name,
                    email=user_entity.email
                )

    @staticmethod
    def get_tenant_codes(session: Session, tenant_ids: List[UUID]):
        if not tenant_ids:
            return []

        tenant_codes = session.query(TenantTable.code).filter(
            col(TenantTable.identifier).in_(tenant_ids),
            TenantTable.is_enabled == true(),
            TenantTable.is_deleted == false()
        ).all()

        return [tenant_code[0] for tenant_code in tenant_codes]

    def get_tenant_by_nile_org_id(self, nile_org_id) -> Optional[TenantInfo]:
        if not nile_org_id:
            return None

        with Session(self.core_db_engine) as session:
            tenant = session.query(TenantTable).filter(
                TenantTable.nile_org_id == nile_org_id,
                TenantTable.is_enabled == true(),
                TenantTable.is_deleted == false()
            ).first()

            if tenant:
                return TenantInfo(
                    identifier=tenant.identifier,
                    name=tenant.name,
                    code=tenant.code,
                    nile_org_id=tenant.nile_org_id
                )
            else:
                return None
