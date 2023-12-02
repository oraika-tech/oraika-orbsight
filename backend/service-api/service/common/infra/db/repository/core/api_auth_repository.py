from typing import List, Optional
from uuid import UUID

from sqlalchemy import Column, true, false
from sqlalchemy.dialects.postgresql import ARRAY, UUID as DB_UUID
from sqlmodel import Field as SqlField, col
from sqlmodel import Session, SQLModel

from service.common.infra.db.db_utils import core_db_engine


class ApiAuthEntity(SQLModel, table=True):
    __tablename__ = "api_auth_master"

    identifier: Optional[UUID] = SqlField(default=None, primary_key=True)
    tenant_ids: List[UUID] = SqlField(sa_column=Column(ARRAY(DB_UUID)))
    name: str
    hashed_key: str
    is_enabled: bool
    is_deleted: bool


def get_api_auth_by_tenant_id(tenant_id: UUID) -> List[ApiAuthEntity]:
    with Session(core_db_engine) as session:
        return session.query(ApiAuthEntity).filter(
            col(ApiAuthEntity.tenant_ids).any(str(tenant_id)),
            ApiAuthEntity.is_enabled == true(),
            ApiAuthEntity.is_deleted == false()
        ).all()
