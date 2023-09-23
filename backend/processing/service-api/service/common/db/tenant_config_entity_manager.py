from typing import Dict, Any, Optional
from uuid import UUID

from sqlalchemy import true, Column, false
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import Session, SQLModel, Field as SqlField

from service.common.db.base_entity_manager import BaseEntityManager


class TenantConfig(SQLModel, table=True):
    __tablename__ = "tenant_config"

    identifier: Optional[UUID] = SqlField(default=None, primary_key=True)
    config_key: str
    config_value: dict = SqlField(default='{}', sa_column=Column(JSONB))
    is_enabled: bool
    is_deleted: bool


class TenantConfigEntityManager(BaseEntityManager):

    def get_tenant_config(self, tenant_id: UUID, config_key: str) -> Dict[Any, Any]:
        with Session(self._get_tenant_engine(tenant_id)) as session:
            tenant_config = session.query(TenantConfig).filter(
                TenantConfig.config_key == config_key,
                TenantConfig.is_deleted == false(),
                TenantConfig.is_enabled == true()
            ).first()
            return tenant_config.config_value if tenant_config else {}
