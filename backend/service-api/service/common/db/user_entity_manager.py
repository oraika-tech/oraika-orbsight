from typing import List, Optional
from uuid import UUID

import bcrypt
from sqlalchemy import Column, true, false
from sqlalchemy.dialects.postgresql import ARRAY, UUID as DB_UUID
from sqlmodel import Field as SqlField
from sqlmodel import Session, SQLModel

from service.auth.domain.base import BasePersistenceManager
from service.common.db.base_entity_manager import BaseEntityManager
from service.common.db.tenant_entity_manager import TenantEntityManager
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


tenant_entity_manager = TenantEntityManager()


class UserEntityManager(BasePersistenceManager, BaseEntityManager):

    def verify_user(self, email: str, password: str) -> Optional[UserInfo]:
        with Session(self.core_db_engine) as session:
            user_entity = session.query(UserTable).filter(
                UserTable.is_deleted == false(),
                UserTable.is_enabled == true(),
                UserTable.email == email
            ).first()

            if user_entity:
                tenants = tenant_entity_manager.get_tenants(session, user_entity.tenant_ids)
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
                tenants = tenant_entity_manager.get_tenants(session, user_entity.tenant_ids)
                return UserInfo(
                    identifier=user_entity.identifier,
                    tenants=tenants,
                    name=user_entity.name,
                    email=user_entity.email
                )
        return None
