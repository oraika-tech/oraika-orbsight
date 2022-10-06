from typing import List, Optional
from uuid import UUID

from sqlalchemy import Column
from sqlalchemy import Text
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import Field as SqlField
from sqlmodel import Session, SQLModel

from service.common.base_entity_manager import BaseEntityManager
from service.visualization.domain.base import BasePersistenceManager
from service.visualization.domain.model.chart_models import ChartDBO, DataSourceType
from service.visualization.domain.model.chart_models import DataSourceSeriesDO
from service.visualization.domain.model.dashboard_models import DashboardDO, ComponentLayoutDO


class DashboardEntity(SQLModel, table=True):
    __tablename__ = "viz_dashboard"

    identifier: Optional[UUID] = SqlField(default=None, primary_key=True)
    frontend_keys: List[str] = SqlField(default='{}', sa_column=Column(ARRAY(Text)))
    title: str
    component_layout: ComponentLayoutDO = SqlField(default='{}', sa_column=Column(JSONB))

    is_enabled: bool
    is_deleted: bool


class ChartEntity(SQLModel, table=True):
    __tablename__ = "viz_chart"

    identifier: Optional[UUID] = SqlField(default=None, primary_key=True)
    data_source_type: DataSourceType
    data_source_series: Optional[List[DataSourceSeriesDO]] = SqlField(default='{}', sa_column=Column(JSONB))
    chart_type: str
    chart_config: Optional[dict] = SqlField(default='{}', sa_column=Column(JSONB))
    data_field_mapping: Optional[List[dict]] = SqlField(default='{}', sa_column=Column(JSONB))

    is_enabled: bool
    is_deleted: bool


class VisualizationDBManager(BasePersistenceManager, BaseEntityManager):

    def get_dashboard(self, tenant_id: UUID, dashboard_id: UUID) -> DashboardDO:
        with Session(self._get_tenant_engine(tenant_id)) as session:
            query = session.query(DashboardEntity).filter(
                DashboardEntity.identifier == dashboard_id,
                DashboardEntity.is_enabled == True,
                DashboardEntity.is_deleted == False
            )
            dashboard = query.first()
            return DashboardDO(
                identifier=dashboard.identifier,
                title=dashboard.title,
                frontend_keys=dashboard.frontend_keys,
                component_layout=dashboard.component_layout
            )

    def get_dashboards(self, tenant_id: UUID, frontend_key: str) -> List[DashboardDO]:
        with Session(self._get_tenant_engine(tenant_id)) as session:
            query = session.query(DashboardEntity).filter(
                DashboardEntity.is_enabled == True,
                DashboardEntity.is_deleted == False
            )
            if frontend_key:
                query = query.filter(
                    DashboardEntity.frontend_keys.any(frontend_key)
                )
            dashboards = query.all()
            return [
                DashboardDO(
                    identifier=dashboard.identifier,
                    title=dashboard.title,
                    frontend_keys=dashboard.frontend_keys,
                    component_layout=dashboard.component_layout
                )
                for dashboard in dashboards
            ]

    def get_charts_by_ids(self, tenant_id: UUID, chart_ids: List[UUID]) -> dict[UUID, ChartDBO]:
        with Session(self._get_tenant_engine(tenant_id)) as session:
            query = session.query(ChartEntity).filter(
                ChartEntity.identifier.in_(chart_ids),
                ChartEntity.is_enabled == True,
                ChartEntity.is_deleted == False
            )
            charts = query.all()
            return {
                chart.identifier: ChartDBO(
                    identifier=chart.identifier,
                    chart_type=chart.chart_type,
                    chart_config=chart.chart_config,
                    data_source_type=chart.data_source_type,
                    data_source_series=chart.data_source_series,
                    data_field_mapping=chart.data_field_mapping
                )
                for chart in charts
            }
