import logging
from typing import List

from fastapi import APIRouter, Depends

from service.app.auth.domain.user_service import get_current_user
from service.app.business.business_models import StatsInfo, TaxonomyInfo
from service.app.business.business_service import enabled_taxonomy_count, get_taxonomy_data

logger = logging.getLogger(__name__)

routes = APIRouter()


@routes.get("", response_model=List[TaxonomyInfo])
def get_taxonomy_data_api(user_info=Depends(get_current_user)):
    return get_taxonomy_data(user_info.preferred_tenant_id)


@routes.get("/stats", response_model=List[StatsInfo])
def taxonomy_count_api(user_info=Depends(get_current_user)):
    return enabled_taxonomy_count(user_info.preferred_tenant_id)
