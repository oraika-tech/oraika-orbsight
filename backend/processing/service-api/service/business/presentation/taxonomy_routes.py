import logging
from typing import List, Optional

from fastapi import Depends, APIRouter, Body

from service.business.domain.model.taxonomy import TaxonomyInfo
from service.business.domain.model.stats import StatsInfo
from service.business import business_domain_handler

from service.common.deps import get_current_user
from starlette.exceptions import HTTPException

logger = logging.getLogger(__name__)


def get_handler():
    return business_domain_handler


routes = APIRouter()


@routes.get("", response_model=List[TaxonomyInfo])
def get_taxonomy_data(
        user_info=Depends(get_current_user), handler=Depends(get_handler)
):
    if not user_info:
        raise HTTPException(status_code=400, detail="User not found")

    return handler.get_taxonomy_data(user_info.company_id)


@routes.get("/stats", response_model=List[StatsInfo])
def taxonomy_count(user_info=Depends(get_current_user), handler=Depends(get_handler)):
    if not user_info:
        raise HTTPException(status_code=400, detail="User not found")

    return handler.taxonomy_count(user_info.company_id)


@routes.get("/types/stats", response_model=List[StatsInfo])
def taxonomy_types_count(user_info=Depends(get_current_user), handler=Depends(get_handler)):
    if not user_info:
        raise HTTPException(status_code=400, detail="User not found")

    return handler.taxonomy_types_count(user_info.company_id)


@routes.get("/categories/stats", response_model=List[StatsInfo])
def categories_count(user_info=Depends(get_current_user), handler=Depends(get_handler)):
    if not user_info:
        raise HTTPException(status_code=400, detail="User not found")

    return handler.categories_count(user_info.company_id)


@routes.get("/categories", response_model=List[str])
def get_categories(user_info=Depends(get_current_user), handler=Depends(get_handler)):
    if not user_info:
        raise HTTPException(status_code=400, detail="User not found")

    return handler.get_categories(user_info.company_id)
