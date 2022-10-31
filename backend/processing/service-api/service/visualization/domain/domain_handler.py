import logging
from typing import List
from uuid import UUID

from cachetools import TTLCache, cached
from pydantic import BaseSettings

from service.common.settings import settings
from service.visualization.domain.dynamic_dashboard.dynamic_dashboard_manager import DynamicDashboardManager
from .base import BasePersistenceManager
from .model.chart_models import FilterDO

logger = logging.getLogger(__name__)


class VisualizationDomainHandler(BaseSettings):
    persistence_manager: BasePersistenceManager
    dynamic_dashboard_manager: DynamicDashboardManager
    hash_prefix: str = "hash_"

    def hash_key_dashboard(self, tenant_id: UUID, tenant_code: str, dashboard_id: UUID, filter_list: List[FilterDO]):
        return self.hash_prefix, tenant_id, tenant_code, dashboard_id, tuple(filter_list)

    def hash_key_dashboards(self, tenant_id: UUID, tenant_code: str, frontend_key: str, include_components: bool):
        return self.hash_prefix, tenant_id, tenant_code, frontend_key, include_components

    @cached(cache=TTLCache(maxsize=settings.CACHE_MAX_SIZE, ttl=settings.CACHE_TTL), key=hash_key_dashboard)
    def get_dashboard(self, tenant_id: UUID, tenant_code: str, dashboard_id: UUID, filter_list: List[FilterDO]):
        dashboard = self.persistence_manager.get_dashboard(tenant_id, dashboard_id)
        return self.dynamic_dashboard_manager.get_updated_dashboard_info(tenant_id, tenant_code,
                                                                         dashboard, filter_list,
                                                                         include_components=True)

    @cached(cache=TTLCache(maxsize=settings.CACHE_MAX_SIZE, ttl=settings.CACHE_TTL), key=hash_key_dashboards)
    def get_dashboards(self, tenant_id: UUID, tenant_code: str, frontend_key: str, include_components: bool):
        dashboards = self.persistence_manager.get_dashboards(tenant_id, frontend_key)
        return [
            self.dynamic_dashboard_manager.get_updated_dashboard_info(tenant_id, tenant_code, dashboard, [],
                                                                      include_components)
            for dashboard in dashboards
        ]
