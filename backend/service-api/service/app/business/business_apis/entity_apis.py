import logging
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Body, Depends
from starlette.exceptions import HTTPException

from service.app.auth.domain.user_service import get_current_user
from service.app.business.business_apis.business_api_models import StatusRequest
from service.app.business.business_service import get_all_entities, enabled_entities_count, get_entity, update_entity_enable_state
from service.app.business.business_models import EntityInfo, StatsInfo

logger = logging.getLogger(__name__)

routes = APIRouter()


@routes.get("", response_model=List[EntityInfo])
def get_all_entities_api(enabled: Optional[bool] = None, user_info=Depends(get_current_user)):
    return get_all_entities(user_info.preferred_tenant_id, enabled)


@routes.get("/stats", response_model=List[StatsInfo])
def enabled_entities_count_api(user_info=Depends(get_current_user)):
    return enabled_entities_count(user_info.preferred_tenant_id)


@routes.get("/{entity_id}", response_model=Optional[EntityInfo])
def get_entity_api(entity_id: UUID, user_info=Depends(get_current_user)):
    entity = get_entity(user_info.preferred_tenant_id, entity_id)
    if not entity:
        raise HTTPException(status_code=404, detail="Entity not found")
    return entity


@routes.patch("/{entity_id}")
def update_entity_enable_state_api_api(
        entity_id: UUID,
        status_request: StatusRequest = Body(...),
        user_info=Depends(get_current_user)):
    return update_entity_enable_state(user_info.preferred_tenant_id, entity_id, status_request.enabled)
