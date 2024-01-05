from typing import List, Optional
from uuid import UUID

from sqlalchemy import Column, true, false
from sqlalchemy.dialects.postgresql import ARRAY, UUID as DB_UUID
from sqlmodel import Field, any_, select
from sqlmodel import Session, SQLModel

from service.common.infra.db.db_utils import core_db_engine


class ApiAuthEntity(SQLModel, table=True):
    __tablename__ = "api_auth_master"

    identifier: Optional[UUID] = Field(default=None, primary_key=True)
    tenant_ids: List[UUID] = Field(sa_column=Column(ARRAY(DB_UUID)))
    name: str
    hashed_key: str
    is_enabled: bool
    is_deleted: bool


def get_api_auth_by_tenant_id(tenant_id: UUID) -> List[ApiAuthEntity]:
    with Session(core_db_engine) as session:
        return list(session.exec(
            select(ApiAuthEntity).where(
                any_(ApiAuthEntity.tenant_ids) == str(tenant_id),
                ApiAuthEntity.is_enabled == true(),
                ApiAuthEntity.is_deleted == false()
            )
        ).all())
