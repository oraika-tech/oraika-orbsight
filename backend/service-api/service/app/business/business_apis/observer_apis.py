import logging
from typing import List, Optional
from uuid import UUID

from fastapi import Depends, APIRouter, Body

from service.app.auth.domain.user_service import get_current_user
from service.app.business.business_apis.business_api_models import StatusRequest
from service.app.business.business_service import get_all_observers, enabled_observers_count, get_observer, update_observer_enable_state
from service.app.business.business_models import ObserverInfo, StatsInfo

logger = logging.getLogger(__name__)

routes = APIRouter()


@routes.get("", response_model=List[ObserverInfo])
def get_all_observers_api(enabled: Optional[bool] = None, user_info=Depends(get_current_user)):
    return get_all_observers(user_info.preferred_tenant_id, enabled)


@routes.get("/stats", response_model=List[StatsInfo])
def enabled_observers_count_api(user_info=Depends(get_current_user)):
    return enabled_observers_count(user_info.preferred_tenant_id)


@routes.get("/{observer_id}", response_model=Optional[ObserverInfo])
def get_observer_api(observer_id: UUID, user_info=Depends(get_current_user)):
    return get_observer(user_info.preferred_tenant_id, observer_id)


@routes.patch("/{observer_id}")
def update_observer_enable_state_api(observer_id: UUID, status_request: StatusRequest = Body(...), user_info=Depends(get_current_user)):
    return update_observer_enable_state(user_info.preferred_tenant_id, observer_id, status_request.enabled)
