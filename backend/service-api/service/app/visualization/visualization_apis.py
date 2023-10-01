import logging
from http import HTTPStatus
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from requests import HTTPError
from starlette.exceptions import HTTPException

from service.app.auth.auth_models import TenantInfo
from service.app.auth.domain.user_service import get_current_user
from service.app.visualization.model.chart_models import FilterDO
from service.app.visualization.model.dashboard_models import DashboardDO
from service.app.visualization.visualization_service import get_dashboard_domain, get_dashboards_domain

logger = logging.getLogger(__name__)

routes = APIRouter()


class DashboardRequest(BaseModel):
    filters: List[FilterDO]


def get_tenant_code(tenants: List[TenantInfo], preferred_tenant_id: UUID):
    selected_tenants = [tenant.code for tenant in tenants if tenant.identifier == preferred_tenant_id]
    return selected_tenants[0] if len(selected_tenants) > 0 else None


@routes.post("/dashboards/{dashboard_id}", response_model=DashboardDO)
def get_dashboard_api(
        dashboard_id: UUID,
        request_body: DashboardRequest,
        user_info=Depends(get_current_user)):
    if not user_info:
        raise HTTPException(status_code=400, detail="User not found")

    filter_list: List[FilterDO] = request_body.filters
    logger.debug("Request filters: %s", filter_list)

    try:
        tenant_code = get_tenant_code(user_info.tenants, user_info.preferred_tenant_id)
        dashboard = get_dashboard_domain(user_info.preferred_tenant_id, tenant_code, dashboard_id, filter_list)
        if dashboard:
            return dashboard
        else:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Dashboard not found")
    except HTTPError as ex:
        raise HTTPException(status_code=ex.response.status_code, detail=ex.response.text)


@routes.get("/dashboards", response_model=List[DashboardDO])
def search_dashboards(
        frontend_key: Optional[str] = None,
        include_components: bool = False,
        user_info=Depends(get_current_user)):
    if not frontend_key:
        raise HTTPException(status_code=400, detail="Frontend key is empty")
    if not user_info:
        raise HTTPException(status_code=400, detail="User not found")

    tenant_code = get_tenant_code(user_info.tenants, user_info.preferred_tenant_id)
    return get_dashboards_domain(user_info.preferred_tenant_id, tenant_code, frontend_key, include_components)
