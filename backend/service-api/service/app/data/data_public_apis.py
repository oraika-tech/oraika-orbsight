import logging
from typing import Any

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel

from service.app.auth.auth_models import AuthInfo
from service.app.auth.domain.client_auth_service import get_api_key
from service.app.common.exception_handler import http_exception, ErrorData
from service.app.data.data_models import TextAnalysisUpdateData, AnalysisData
from service.app.data.data_service import (update_text_analysis_data, get_analysis_data)

logger = logging.getLogger(__name__)

routes = APIRouter()  # route_class=TimedRoute)


class UpdateResponse(BaseModel):
    message: str
    data: dict


@routes.get("/analysis/{data_id}", response_description="Get Analysis Data", response_model=AnalysisData, responses={
    401: {"model": ErrorData, "description": "Invalid API Key or tenant code"},
    404: {"model": ErrorData, "description": "No data found for the given ID"},
    422: {"model": ErrorData, "description": "Validation error"}
})
def get_analysis_data_api(
        data_id: int,
        auth_info: AuthInfo = Depends(get_api_key)) -> AnalysisData:
    """
       Gets the analysis data for a given data id.
       - **data_id**: The unique identifier for the data.

       The endpoint returns the analysis data for the given data id.
    """
    analysis_data = get_analysis_data(auth_info.tenant_id, data_id)
    if analysis_data:
        return analysis_data
    else:
        raise http_exception(status_code=status.HTTP_404_NOT_FOUND, msg="Id %d not found" % data_id)


@routes.patch("/analysis/{data_id}", response_description="Update Analysis Data", response_model=UpdateResponse, responses={
    400: {"model": ErrorData, "description": "Bad request or nothing to update"},
    401: {"model": ErrorData, "description": "Invalid API Key or tenant code"},
    404: {"model": ErrorData, "description": "No data found for the given ID"},
    422: {"model": ErrorData, "description": "Validation error"}
})
def update_analysis_data_api(
        data_id: int,
        update_data: TextAnalysisUpdateData,
        auth_info: AuthInfo = Depends(get_api_key)):
    """
       Updates the analysis data for a given data id.

       - **data_id**: The unique identifier for the data.
       - **update_data**: Object containing the fields to be updated.
            - At least one of the fields is required - **sentiment**, **departments**, **activities**, **people**.
            - All array fields will be completely overwritten. E.g if the current departments are ['A', 'B'] and the
                new departments are ['C', 'D'], the new departments will be ['C', 'D'] and not ['A', 'B', 'C', 'D'].

       The endpoint allows updating various fields like sentiment, departments, activities, and people related to the analysis data.
       Note: API is idempotent. If the same request is sent multiple times, the result will be the same.
    """

    # checking empty element of each array field
    for field in ['departments', 'activities', 'people']:
        values = getattr(update_data, field)
        if values is not None:
            for value in values:
                if len(value.strip()) == 0:
                    raise http_exception(status_code=status.HTTP_400_BAD_REQUEST,
                                         msg=f"Empty element in array for field {field}")

    update_data_dict: dict[str, Any] = {'raw_data_id': data_id}
    if update_data.sentiment is not None:
        update_data_dict['emotion'] = update_data.sentiment

    if update_data.departments is not None:
        update_data_dict['taxonomy_tags'] = update_data.departments

    if update_data.activities is not None:
        update_data_dict['taxonomy_terms'] = update_data.activities

    if update_data.people is not None:
        update_data_dict['people'] = update_data.people

    if len(update_data_dict) > 1:
        row_count = update_text_analysis_data(auth_info.tenant_id, update_data_dict)
        if row_count == 1:
            update_data_map = {key: value for key, value in update_data.dict().items() if value is not None}
            return UpdateResponse(message='Update successful', data=update_data_map)
        elif row_count == 0:
            raise http_exception(status_code=status.HTTP_404_NOT_FOUND,
                                 msg="Id %d not found" % data_id)
        else:
            logger.error(f"Multiple rows updated for id {data_id}")
            raise http_exception(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                 msg="Multiple rows updated for id %d" % data_id)
    else:
        raise http_exception(status_code=status.HTTP_400_BAD_REQUEST, msg="Nothing to update", data=update_data.dict())
