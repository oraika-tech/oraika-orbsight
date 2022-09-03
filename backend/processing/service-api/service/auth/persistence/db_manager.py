from typing import List, Optional
from uuid import UUID

import bcrypt
from service.auth.domain.base import BasePersistenceManager
from service.common.base_entity_manager import BaseEntityManager
from service.common.model.user import UserInfo
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import ARRAY, UUID as DB_UUID
from sqlmodel import Field as SqlField
from sqlmodel import Session, SQLModel


class UserTable(SQLModel, table=True):
    __tablename__ = "user_master"

    identifier: Optional[UUID] = SqlField(default=None, primary_key=True)
    tenant_ids: List[UUID] = SqlField(sa_column=Column(ARRAY(DB_UUID)))
    name: str
    email: str
    hash_password: str
    is_enabled: bool
    is_deleted: bool


class UserDBManager(BasePersistenceManager, BaseEntityManager):

    def verify_user(self, email: str, password: str) -> Optional[UserInfo]:
        with Session(self.core_db_engine) as session:
            user_entity = session.query(UserTable).filter(
                UserTable.is_deleted == False,
                UserTable.is_enabled == True,
                UserTable.email == email
            ).first()

            if user_entity is not None:
                if bcrypt.checkpw(password.encode(), user_entity.hash_password.encode()):
                    return UserInfo(
                        identifier=user_entity.identifier,
                        tenant_ids=user_entity.tenant_ids,
                        name=user_entity.name,
                        email=user_entity.email
                    )

    def get_user(self, user_id: str) -> Optional[UserInfo]:
        with Session(self.core_db_engine) as session:
            user_entity = session.query(UserTable).filter(
                UserTable.identifier == user_id,
                UserTable.is_enabled == True,
                UserTable.is_deleted == False,
            ).first()

            if user_entity is not None:
                return UserInfo(
                    identifier=user_entity.identifier,
                    tenant_ids=user_entity.tenant_ids,
                    name=user_entity.name,
                    email=user_entity.email
                )
