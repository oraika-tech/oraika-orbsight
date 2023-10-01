import logging
from typing import List

from fastapi import APIRouter, Depends
from starlette.exceptions import HTTPException

from service.app.auth.domain.user_service import get_current_user
from service.app.business.business_service import get_categories, enabled_categories_count
from service.app.auth.auth_models import UserInfo
from service.app.business.business_models import CategoryInfo, StatsInfo

logger = logging.getLogger(__name__)

routes = APIRouter()


@routes.get("", response_model=List[CategoryInfo])
def get_categories_api(user_info: UserInfo = Depends(get_current_user)):
    if not user_info:
        raise HTTPException(status_code=400, detail="User not found")
    if not user_info.preferred_tenant_id:
        raise HTTPException(status_code=400, detail="No preferred tenant for user")

    return get_categories(user_info.preferred_tenant_id)


@routes.get("/stats", response_model=List[StatsInfo])
def categories_count_api(user_info=Depends(get_current_user)):
    if not user_info:
        raise HTTPException(status_code=400, detail="User not found")

    return enabled_categories_count(user_info.preferred_tenant_id)
