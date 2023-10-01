import logging
from typing import List
from uuid import UUID

from cachetools import TTLCache, cached

from service.app.visualization import visualization_db_provider as db_provider
from service.app.visualization.dynamic_dashboard.dynamic_dashboard_service import get_updated_dashboard_info
from service.app.visualization.model.chart_models import FilterDO
from service.common.config.app_settings import app_settings

logger = logging.getLogger(__name__)

hash_prefix: str = "hash_"


def hash_key_dashboard(tenant_id: UUID, tenant_code: str, dashboard_id: UUID, filter_list: List[FilterDO]):
    return hash_prefix, tenant_id, tenant_code, dashboard_id, tuple(filter_list)


def hash_key_dashboards(tenant_id: UUID, tenant_code: str, frontend_key: str, include_components: bool):
    return hash_prefix, tenant_id, tenant_code, frontend_key, include_components


@cached(cache=TTLCache(maxsize=app_settings.CACHE_MAX_SIZE, ttl=app_settings.CACHE_TTL), key=hash_key_dashboard)
def get_dashboard_domain(tenant_id: UUID, tenant_code: str, dashboard_id: UUID, filter_list: List[FilterDO]):
    dashboard = db_provider.get_dashboard_dp(tenant_id, dashboard_id)
    if not dashboard:
        return None
    return get_updated_dashboard_info(tenant_id, tenant_code, dashboard, filter_list, include_components=True)


@cached(cache=TTLCache(maxsize=app_settings.CACHE_MAX_SIZE, ttl=app_settings.CACHE_TTL), key=hash_key_dashboards)
def get_dashboards_domain(tenant_id: UUID, tenant_code: str, frontend_key: str, include_components: bool):
    dashboards = db_provider.get_dashboards_dp(tenant_id, frontend_key)
    return [get_updated_dashboard_info(tenant_id, tenant_code, dashboard, [], include_components)
            for dashboard in dashboards]
