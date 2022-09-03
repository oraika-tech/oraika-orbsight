import logging
from typing import Any, Dict, List

from fastapi import APIRouter, Depends
from service.common.deps import get_current_user
from service.data import grafana_service
from starlette.exceptions import HTTPException

logger = logging.getLogger(__name__)


def get_handler():
    return grafana_service


routes = APIRouter()

GRAFANA_HOST_URL = 'https://grafana.oraika.com/api/alertmanager/grafana/api/v2',


@routes.get("/alerts", response_model=List[Dict[str, Any]])
def get_alerts_data(
        user_info=Depends(get_current_user),
        handler=Depends(get_handler)):
    if not user_info:
        raise HTTPException(status_code=400, detail="User not found")

    return handler.get_alerts()
