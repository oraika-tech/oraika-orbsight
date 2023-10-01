from typing import Optional, List
from uuid import UUID

from sqlalchemy import Column, Enum as SqlEnum, true, false
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import SQLModel, Field as SqlField, Session, col

from service.common.infra.db.db_utils import get_tenant_engine
from service.common.models import DataSourceType, DataSourceSeriesDO, DataMapping


class ChartEntity(SQLModel, table=True):
    __tablename__ = "viz_chart"

    identifier: Optional[UUID] = SqlField(default=None, primary_key=True)
    data_source_type: DataSourceType = SqlField(sa_column=Column(SqlEnum(DataSourceType)))
    data_source_series: Optional[List[DataSourceSeriesDO]] = SqlField(default='{}', sa_column=Column(JSONB))
    chart_type: str
    chart_config: Optional[dict] = SqlField(default='{}', sa_column=Column(JSONB))
    data_transformer_meta: Optional[DataMapping] = SqlField(default='{}', sa_column=Column(JSONB))

    is_enabled: bool
    is_deleted: bool


def get_charts_by_ids(tenant_id: UUID, chart_ids: List[UUID]) -> list[ChartEntity]:
    with Session(get_tenant_engine(tenant_id)) as session:
        return session.query(ChartEntity).filter(
            col(ChartEntity.identifier).in_(chart_ids),
            ChartEntity.is_enabled == true(),
            ChartEntity.is_deleted == false()
        ).all()
