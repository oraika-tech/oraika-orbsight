import logging
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from requests import HTTPError
from starlette.exceptions import HTTPException

from service.common.deps import get_current_user
from service.visualization import domain_handler
from service.visualization.domain.model.chart_models import FilterDO
from service.visualization.domain.model.dashboard_models import DashboardDO

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def get_handler():
    return domain_handler


routes = APIRouter()


class DashboardRequest(BaseModel):
    filters: List[FilterDO]


@routes.post("/dashboards/{dashboard_id}", response_model=DashboardDO)
def get_dashboard(
        dashboard_id: UUID,
        request_body: DashboardRequest,
        user_info=Depends(get_current_user),
        handler=Depends(get_handler)):
    if not user_info:
        raise HTTPException(status_code=400, detail="User not found")

    filter_list: List[FilterDO] = request_body.filters
    logger.info(f"FILTERS:{filter_list}")

    try:
        return handler.get_dashboard(user_info.tenant_ids[0], user_info.tenant_codes[0], dashboard_id, filter_list)
    except HTTPError as ex:
        raise HTTPException(status_code=ex.response.status_code, detail=ex.response.text)


@routes.get("/dashboards", response_model=List[DashboardDO])
def search_dashboards(
        frontend_key: Optional[str] = None,
        include_components: bool = False,
        user_info=Depends(get_current_user),
        handler=Depends(get_handler)):
    if not user_info:
        raise HTTPException(status_code=400, detail="User not found")

    return handler.get_dashboards(user_info.tenant_ids[0], user_info.tenant_codes[0], frontend_key, include_components)
