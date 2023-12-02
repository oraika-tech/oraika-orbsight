from typing import Optional
from uuid import UUID

from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import Field as SqlField
from sqlmodel import Session, SQLModel

from service.common.infra.db.db_utils import core_db_engine


class ApiLogAuditEntity(SQLModel, table=True):
    __tablename__ = "api_log_audit"

    identifier: Optional[int] = SqlField(default=None, primary_key=True)

    # Request
    request_url: str
    request_method: str
    request_headers: dict = SqlField(default='{}', sa_column=Column(JSONB))
    request_body: Optional[dict] = SqlField(default=None, sa_column=Column(JSONB))

    # Response
    response_headers: dict = SqlField(default='{}', sa_column=Column(JSONB))
    response_body: Optional[dict] = SqlField(default=None, sa_column=Column(JSONB))
    status_code: int
    processing_time: float

    # Client
    tenant_id: Optional[UUID]
    user_id: Optional[UUID]
    api_auth_id: Optional[UUID]


def insert_api_log_audit(api_log_audit: ApiLogAuditEntity) -> ApiLogAuditEntity:
    with Session(core_db_engine) as session:
        session.add(api_log_audit)
        session.commit()
        session.refresh(api_log_audit)
        return api_log_audit
