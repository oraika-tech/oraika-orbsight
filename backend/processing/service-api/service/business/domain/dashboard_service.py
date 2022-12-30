from typing import Dict, List
from uuid import UUID

from cachetools import TTLCache, cached
from pydantic import BaseSettings

from service.common.settings import settings
from .base import BasePersistenceManager


class DashboardService(BaseSettings):
    persistence_manager: BasePersistenceManager
    panel_dashboard: Dict[str, dict] = {}

    def hash_key_for_dashboard(self, tenant_id: UUID):
        return tenant_id

    def hash_key_for_panel(self, tenant_id: UUID, panel_name: str):
        return (
            tenant_id,
            panel_name
        )

    @cached(cache=TTLCache(maxsize=settings.CACHE_MAX_SIZE, ttl=settings.CACHE_TTL), key=hash_key_for_dashboard)
    def get_dashboards(self, tenant_id: UUID) -> List[dict]:
        return self.persistence_manager.get_dashboards(tenant_id)

    @cached(cache=TTLCache(maxsize=settings.CACHE_MAX_SIZE, ttl=settings.CACHE_TTL), key=hash_key_for_panel)
    def get_dashboard_panel_data(self, tenant_id: UUID, panel_name: str) -> dict:
        panel_info = self.persistence_manager.get_panels(tenant_id)
        if panel_info is not None:
            return panel_info[panel_name]
        else:
            return {}
