import logging
from typing import List

from fastapi import APIRouter, Depends
from starlette.exceptions import HTTPException

from service.business import dashboard_handler
from service.common.deps import get_current_user

logger = logging.getLogger(__name__)


def get_handler():
    return dashboard_handler


routes = APIRouter()


@routes.get("", response_model=List[dict])
def get_dashboard_data(
        user_info=Depends(get_current_user),
        handler=Depends(get_handler)):
    if not user_info:
        raise HTTPException(status_code=400, detail="User not found")

    return handler.get_dashboards(user_info.preferred_tenant_id)


@routes.get("/panels", response_model=dict)
def get_live_feed_dashboard_data(
        panel: str,
        user_info=Depends(get_current_user),
        handler=Depends(get_handler)):
    if not user_info:
        raise HTTPException(status_code=400, detail="User not found")

    return handler.get_dashboard_panel_data(user_info.preferred_tenant_id, panel)
