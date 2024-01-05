from typing import Optional
from uuid import UUID

from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import SQLModel, Field


class TenantGlobalConfig(SQLModel, table=True):
    __tablename__ = "tenant_global_config"

    identifier: Optional[UUID] = Field(default=None, primary_key=True)
    tenant_id: UUID
    config_key: str
    config_value: dict = Field(default='{}', sa_column=Column(JSONB))
