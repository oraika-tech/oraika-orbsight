from typing import Optional, Dict, Any
from uuid import UUID

from sqlalchemy import Column, false, true
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import SQLModel, Field, Session, select

from service.common.infra.db.db_utils import get_tenant_engine


class TenantConfig(SQLModel, table=True):
    __tablename__ = "tenant_config"

    identifier: Optional[UUID] = Field(default=None, primary_key=True)
    config_key: str
    config_value: dict = Field(default='{}', sa_column=Column(JSONB))
    is_enabled: bool
    is_deleted: bool


def get_tenant_config(tenant_id: UUID, config_key: str) -> Dict[Any, Any]:
    with Session(get_tenant_engine(tenant_id)) as session:
        tenant_config = session.exec(select(TenantConfig).where(
            TenantConfig.config_key == config_key,
            TenantConfig.is_deleted == false(),
            TenantConfig.is_enabled == true()
        )).first()
        return tenant_config.config_value if tenant_config else {}
