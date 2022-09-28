from abc import abstractmethod
from typing import List
from uuid import UUID

from pydantic import BaseSettings

from service.visualization.domain.model.chart_models import ChartDBO
from service.visualization.domain.model.dashboard_models import DashboardDO


class BasePersistenceManager(BaseSettings):

    @abstractmethod
    def get_dashboard(self, tenant_id: UUID, dashboard_id: UUID) -> DashboardDO:
        pass

    @abstractmethod
    def get_dashboards(self, tenant_id: UUID, frontend_key: str) -> List[DashboardDO]:
        pass

    @abstractmethod
    def get_charts_by_ids(self, tenant_id: UUID, chart_ids: List[UUID]) -> dict[UUID, ChartDBO]:
        pass
