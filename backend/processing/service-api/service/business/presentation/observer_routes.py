import logging
from typing import List, Optional
from uuid import UUID

from fastapi import Depends, APIRouter, Body

from service.business.domain.model.observer import ObserverInfo
from service.business.domain.model.stats import StatsInfo
from service.business import business_domain_handler

from service.common.deps import get_current_user
from starlette.exceptions import HTTPException
from .request import StatusRequest

logger = logging.getLogger(__name__)


def get_handler():
    return business_domain_handler


routes = APIRouter()


@routes.get("", response_model=List[ObserverInfo])
def get_all_observers(
        enabled: Optional[bool] = None, user_info=Depends(get_current_user), handler=Depends(get_handler)
):
    if not user_info:
        raise HTTPException(status_code=400, detail="User not found")

    return handler.get_all_observers(user_info.tenant_ids[0], enabled)


@routes.get("/stats", response_model=List[StatsInfo])
def enabled_observers_count(user_info=Depends(get_current_user), handler=Depends(get_handler)):
    if not user_info:
        raise HTTPException(status_code=400, detail="User not found")

    return handler.enabled_observers_count(user_info.tenant_ids[0])


@routes.get("/{observer_id}", response_model=Optional[ObserverInfo])
def get_observer(observer_id: UUID, user_info=Depends(get_current_user), handler=Depends(get_handler)):
    if not user_info:
        raise HTTPException(status_code=400, detail="User not found")

    return handler.get_observer(user_info.tenant_ids[0], observer_id)


@routes.patch("/{observer_id}")
def update_observer_enable_state(
        observer_id: UUID, status_request: StatusRequest = Body(...), user_info=Depends(get_current_user),
        handler=Depends(get_handler)
):
    if not user_info:
        raise HTTPException(status_code=400, detail="User not found")

    return handler.update_observer_enable_state(user_info.tenant_ids[0], observer_id, status_request.enabled)
