import logging
from datetime import date, datetime
from typing import Optional, List, Union

from fastapi import APIRouter, Depends

from service.data import data_domain_handler
from service.data.domain.model.processed_data import ProcessedDataInfo
from .response import DataResponse

from service.common.deps import get_current_user
from starlette.exceptions import HTTPException

logger = logging.getLogger(__name__)


def get_handler():
    return data_domain_handler


routes = APIRouter()


@routes.get("", response_model=List[DataResponse])
def get_processed_data_with_raw_data(
    start_date: Union[datetime, date] = None,
    end_date: Union[datetime, date] = None,
    text_lang: Optional[str] = 'en',
    entity_name: Optional[str] = 'All',
    observer_type: Optional[str] = 'All',
    user_info=Depends(get_current_user),
    handler=Depends(get_handler)
):
    if not user_info:
        raise HTTPException(status_code=400, detail="User not found")

    processed_data = handler.get_processed_data_with_raw_data(
        company_id=user_info.company_id,
        start_date=start_date,
        end_date=end_date,
        text_lang=text_lang,
        entity_name=entity_name,
        observer_type=observer_type
    )

    return [
        DataResponse(
            text="" if not data.raw_data else data.raw_data.raw_text,
            emotion=data.emotion
        )
        for data in processed_data
    ]


@routes.get("/entities", response_model=Optional[List[str]])
def get_distinct_entity_names(
    user_info=Depends(get_current_user), handler=Depends(get_handler)
):
    if not user_info:
        raise HTTPException(status_code=400, detail="User not found")

    return handler.get_distinct_entity_names(user_info.company_id)


@routes.get("/observers", response_model=Optional[List[str]])
def get_distinct_observer_types(
    user_info=Depends(get_current_user), handler=Depends(get_handler)
):
    if not user_info:
        raise HTTPException(status_code=400, detail="User not found")

    return handler.get_distinct_observer_types(user_info.company_id)
