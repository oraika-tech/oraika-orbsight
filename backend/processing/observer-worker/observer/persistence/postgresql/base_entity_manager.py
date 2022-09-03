from typing import Any, Dict, Optional
from uuid import UUID

from pydantic import BaseSettings, Field
from sqlalchemy import Column, select
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import Field as SqlField
from sqlmodel import Session, SQLModel, create_engine


class TenantGlobalConfig(SQLModel, table=True):
    __tablename__ = "tenant_global_config"

    identifier: Optional[UUID] = SqlField(default=None, primary_key=True)
    tenant_id: UUID
    config_key: str
    config_value: dict = SqlField(default='{}', sa_column=Column(JSONB))


class BaseEntityManager(BaseSettings):
    db_host: Optional[str] = Field("localhost:5432", env='DB_HOST')
    core_db_name: str = Field("orb_core", env='CORE_DB_NAME')
    core_db_user: str = Field("orbsight", env='CORE_DB_USER')
    core_db_password: str = Field("orbsight", env='CORE_DB_PASSWORD')
    db_engine_name: str = Field("postgresql", env="DB_ENGINE_NAME")
    core_db_engine: Any
    tenant_db_engines: Dict[UUID, Any] = {}

    def __init__(self, **values: Any):
        super().__init__(**values)
        connection_string = \
            f"{self.db_engine_name}://{self.core_db_user}:{self.core_db_password}@{self.db_host}/{self.core_db_name}"
        self.core_db_engine = create_engine(connection_string)

    def _get_tenant_engine(self, tenant_id: UUID):
        if tenant_id not in self.tenant_db_engines:
            with Session(self.core_db_engine) as session:
                query = select(TenantGlobalConfig) \
                    .filter(TenantGlobalConfig.tenant_id == tenant_id) \
                    .filter(TenantGlobalConfig.config_key == "connection_info")
                config = self._execute_query(session, query)[0].config_value
                db_engine_name = config['db_engine_name'] or self.db_engine_name
                db_user = config.get('db_user', self.core_db_user)
                db_password = config.get('db_password', self.core_db_password)
                db_name = config['db_name']
                connection_string = f"{db_engine_name}://{db_user}:{db_password}@{self.db_host}/{db_name}"
            self.tenant_db_engines[tenant_id] = create_engine(connection_string)
        return self.tenant_db_engines[tenant_id]

    @staticmethod
    def _execute_query(session, query):
        row_list = session.exec(query)
        if row_list is not None:
            return [row[0] for row in row_list]
        else:
            return []
