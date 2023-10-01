from typing import Optional, List
from uuid import UUID

from service.app.visualization.model.chart_models import ChartDBO
from service.app.visualization.model.dashboard_models import DashboardDO
from service.common.infra.db.repository.viz.chart_repository import get_charts_by_ids
from service.common.infra.db.repository.viz.dashboard_repository import get_dashboard, get_dashboards
from service.common.utils.reflection_utils import convert_model, convert_models


def get_dashboard_dp(tenant_id: UUID, dashboard_id: UUID) -> Optional[DashboardDO]:
    dashboards = get_dashboard(tenant_id, dashboard_id)
    return convert_model(dashboards, DashboardDO)


def get_dashboards_dp(tenant_id: UUID, frontend_key: str) -> List[DashboardDO]:
    dashboards = get_dashboards(tenant_id, frontend_key)
    return convert_models(dashboards, DashboardDO)


def get_charts_dp(tenant_id: UUID, chart_ids: List[UUID]) -> list[ChartDBO]:
    charts = get_charts_by_ids(tenant_id, chart_ids)
    return convert_models(charts, ChartDBO)
