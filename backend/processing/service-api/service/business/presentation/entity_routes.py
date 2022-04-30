import logging
from typing import List, Optional

from fastapi import Depends, APIRouter, Body

from service.business.domain.model.entity import EntityInfo
from service.business.domain.model.stats import StatsInfo
from service.business import business_domain_handler

from service.common.deps import get_current_user
from starlette.exceptions import HTTPException
from .request import StatusRequest

logger = logging.getLogger(__name__)


def get_handler():
    return business_domain_handler


routes = APIRouter()


@routes.get("", response_model=List[EntityInfo])
def get_all_entities(
        enabled: Optional[bool] = None, user_info=Depends(get_current_user), handler=Depends(get_handler)
):
    if not user_info:
        raise HTTPException(status_code=400, detail="User not found")

    return handler.get_all_entities(user_info.company_id, enabled)


@routes.get("/stats", response_model=List[StatsInfo])
def enabled_entities_count(user_info=Depends(get_current_user), handler=Depends(get_handler)):
    if not user_info:
        raise HTTPException(status_code=400, detail="User not found")

    return handler.enabled_entities_count(user_info.company_id)


@routes.get("/types/stats", response_model=List[StatsInfo])
def entities_type_count(user_info=Depends(get_current_user), handler=Depends(get_handler)):
    if not user_info:
        raise HTTPException(status_code=400, detail="User not found")

    return handler.entities_type_count(user_info.company_id)


@routes.get("/{entity_id}", response_model=Optional[EntityInfo])
def get_entity(entity_id: int, user_info=Depends(get_current_user), handler=Depends(get_handler)):
    if not user_info:
        raise HTTPException(status_code=400, detail="User not found")

    return handler.get_entity(user_info.company_id, entity_id)


@routes.patch("/{entity_id}")
def update_entity_enable_state(
        entity_id: int, status_request: StatusRequest = Body(...), user_info=Depends(get_current_user),
        handler=Depends(get_handler)
):
    if not user_info:
        raise HTTPException(status_code=400, detail="User not found")

    return handler.update_entity_enable_state(user_info.company_id, entity_id, status_request.enabled)
