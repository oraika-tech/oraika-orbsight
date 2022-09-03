import logging
from typing import List

from fastapi import APIRouter, Depends
from starlette.exceptions import HTTPException

from service.business import business_domain_handler
from service.business.domain.model.category import CategoryInfo
from service.business.domain.model.stats import StatsInfo
from service.common.deps import get_current_user

logger = logging.getLogger(__name__)


def get_handler():
    return business_domain_handler


routes = APIRouter()


@routes.get("", response_model=List[CategoryInfo])
def get_categories(user_info=Depends(get_current_user), handler=Depends(get_handler)):
    if not user_info:
        raise HTTPException(status_code=400, detail="User not found")

    return handler.get_categories(user_info.tenant_ids[0])


@routes.get("/stats", response_model=List[StatsInfo])
def categories_count(user_info=Depends(get_current_user), handler=Depends(get_handler)):
    if not user_info:
        raise HTTPException(status_code=400, detail="User not found")

    return handler.enabled_categories_count(user_info.tenant_ids[0])
