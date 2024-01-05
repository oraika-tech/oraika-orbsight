from typing import List, Optional
from uuid import UUID

from sqlalchemy import Column, true, false
from sqlalchemy.dialects.postgresql import ARRAY, UUID as DB_UUID
from sqlmodel import Field, select
from sqlmodel import Session, SQLModel

from service.common.infra.db.db_utils import core_db_engine


class UserEntity(SQLModel, table=True):
    __tablename__ = "user_master"

    identifier: Optional[UUID] = Field(default=None, primary_key=True)
    tenant_ids: List[UUID] = Field(sa_column=Column(ARRAY(DB_UUID)))
    name: str
    email: str
    hash_password: str
    is_enabled: bool
    is_deleted: bool


def get_user_by_id(user_id: str) -> Optional[UserEntity]:
    with Session(core_db_engine) as session:
        return session.exec(
            select(UserEntity).where(
                UserEntity.identifier == user_id,
                UserEntity.is_enabled == true(),
                UserEntity.is_deleted == false()
            )
        ).first()


def get_user_by_email(email: str) -> Optional[UserEntity]:
    with Session(core_db_engine) as session:
        return session.exec(
            select(UserEntity).where(
                UserEntity.is_deleted == false(),
                UserEntity.is_enabled == true(),
                UserEntity.email == email
            )
        ).first()
