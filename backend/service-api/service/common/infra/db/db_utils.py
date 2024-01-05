from typing import Any, Dict
from uuid import UUID

from sqlalchemy.engine import Engine
from sqlmodel import Session, create_engine, select

from service.common.config.app_settings import app_settings
from service.common.infra.db.repository.core.global_config import TenantGlobalConfig

tenant_db_engines: Dict[UUID, Any] = {}
core_db_engine = create_engine(
    f"{app_settings.DB_ENGINE_NAME}://{app_settings.CORE_DB_USER}:{app_settings.CORE_DB_PASSWORD}@{app_settings.DB_HOST}/{app_settings.CORE_DB_NAME}",
    pool_size=2, pool_pre_ping=True)


def get_tenant_engine(tenant_id: UUID) -> Engine:
    if tenant_id not in tenant_db_engines or not tenant_db_engines[tenant_id]:
        with Session(core_db_engine) as session:
            query = select(TenantGlobalConfig) \
                .where(TenantGlobalConfig.tenant_id == tenant_id) \
                .where(TenantGlobalConfig.config_key == "connection_info")
            config = session.exec(query).one().config_value
            core_db_engine_name = config['db_engine_name'] or app_settings.DB_ENGINE_NAME
            db_user = config.get('db_user', app_settings.CORE_DB_USER)
            db_password = config.get('db_password', app_settings.CORE_DB_PASSWORD)
            db_name = config['db_name']
            connection_string = f"{core_db_engine_name}://{db_user}:{db_password}@{app_settings.DB_HOST}/{db_name}"
        tenant_db_engines[tenant_id] = create_engine(connection_string, pool_size=2, pool_pre_ping=True)
    return tenant_db_engines[tenant_id]
