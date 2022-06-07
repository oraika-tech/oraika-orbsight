import logging
from datetime import date, datetime
from typing import Optional, List, Union

from fastapi import APIRouter, Depends
from service.data.domain.model.dashboard_data import DashboardData
from service.data.domain.model.term import DataTerm
from starlette.exceptions import HTTPException

from service.common.deps import get_current_user
from service.data import data_domain_handler, dashboard_service
from ..domain.model.text_analysis_data import TextAnalysisData
from ..domain.model.entity import DataEntity
from ..domain.model.source_type import DataSourceType
from ..domain.model.key_phrase import EmotionKeyPhrases
from ..domain.model.word_freq import EmotionWordFrequency
from ..domain.model.filter_query_params import FilterQueryParams

logger = logging.getLogger(__name__)


def get_handler():
    return data_domain_handler


def get_dashboard_service():
    return dashboard_service


routes = APIRouter()


@routes.get("/text", response_model=List[TextAnalysisData])
def get_raw_and_processed(
        start_date: Union[datetime, date] = None,
        end_date: Union[datetime, date] = None,
        limit: Optional[int] = None,
        text_lang: Optional[str] = 'en',
        entity_name: Optional[str] = 'All',
        term: Optional[str] = 'All',
        observer_type: Optional[str] = 'All',
        emotion: Optional[str] = 'All',
        user_info=Depends(get_current_user),
        handler=Depends(get_handler)):
    if not user_info:
        raise HTTPException(status_code=400, detail="User not found")

    return handler.get_text_analysis_data(FilterQueryParams(
        company_id=user_info.company_id,
        start_date=start_date,
        end_date=end_date,
        lang_code=text_lang,
        entity_name=entity_name,
        term=term,
        observer_type=observer_type,
        emotion=emotion,
        limit=limit
    ))


@routes.get("/languages", response_model=List[str], response_model_exclude_none=True)
def get_languages_from_data(
        start_date: Union[datetime, date] = None,
        end_date: Union[datetime, date] = None,
        entity_name: Optional[str] = 'All',
        term: Optional[str] = 'All',
        observer_type: Optional[str] = 'All',
        emotion: Optional[str] = 'All',
        user_info=Depends(get_current_user),
        handler=Depends(get_handler)):
    return handler.get_languages(FilterQueryParams(
        company_id=user_info.company_id,
        start_date=start_date,
        end_date=end_date,
        entity_name=entity_name,
        term=term,
        observer_type=observer_type,
        emotion=emotion
    ))


@routes.get("/entities", response_model=List[DataEntity], response_model_exclude_none=True)
def get_unique_entities_from_data(
        start_date: Union[datetime, date] = None,
        end_date: Union[datetime, date] = None,
        text_lang: Optional[str] = 'en',
        term: Optional[str] = 'All',
        observer_type: Optional[str] = None,
        emotion: Optional[str] = None,
        user_info=Depends(get_current_user),
        handler=Depends(get_handler)):
    return handler.get_data_entities(FilterQueryParams(
        company_id=user_info.company_id,
        start_date=start_date,
        end_date=end_date,
        term=term,
        lang_code=text_lang,
        observer_type=observer_type,
        emotion=emotion
    ))


@routes.get("/terms", response_model=List[DataTerm], response_model_exclude_none=True)
def get_unique_terms_from_data(
        start_date: Union[datetime, date] = None,
        end_date: Union[datetime, date] = None,
        text_lang: Optional[str] = 'en',
        entity_name: Optional[str] = 'All',
        observer_type: Optional[str] = None,
        emotion: Optional[str] = None,
        user_info=Depends(get_current_user),
        handler=Depends(get_handler)):
    return handler.get_data_terms(FilterQueryParams(
        company_id=user_info.company_id,
        start_date=start_date,
        end_date=end_date,
        entity_name=entity_name,
        lang_code=text_lang,
        observer_type=observer_type,
        emotion=emotion
    ))


@routes.get("/source-types", response_model=List[DataSourceType], response_model_exclude_none=True)
def get_data_sources_from_data(
        start_date: Union[datetime, date] = None,
        end_date: Union[datetime, date] = None,
        text_lang: Optional[str] = 'en',
        entity_name: Optional[str] = 'All',
        term: Optional[str] = 'All',
        emotion: Optional[str] = 'All',
        user_info=Depends(get_current_user),
        handler=Depends(get_handler)):
    return handler.get_data_sources_types(FilterQueryParams(
        company_id=user_info.company_id,
        start_date=start_date,
        end_date=end_date,
        lang_code=text_lang,
        entity_name=entity_name,
        term=term,
        emotion=emotion
    ))


@routes.get("/key-phrases", response_model=List[EmotionKeyPhrases], response_model_exclude_none=True)
def get_key_phrases_from_data(
        start_date: Union[datetime, date] = None,
        end_date: Union[datetime, date] = None,
        text_lang: Optional[str] = 'en',
        entity_name: Optional[str] = 'All',
        term: Optional[str] = 'All',
        observer_type: Optional[str] = 'All',
        emotion: Optional[str] = 'All',
        limit: Optional[int] = None,
        user_info=Depends(get_current_user),
        handler=Depends(get_handler)):
    if not user_info:
        raise HTTPException(status_code=400, detail="User not found")

    return handler.get_key_phrases(FilterQueryParams(
        company_id=user_info.company_id,
        start_date=start_date,
        end_date=end_date,
        entity_name=entity_name,
        term=term,
        lang_code=text_lang,
        observer_type=observer_type,
        emotion=emotion,
        limit=limit
    ))


@routes.get("/word-cloud", response_model=List[EmotionWordFrequency])
def get_word_cloud_from_data(
        start_date: Union[datetime, date] = None,
        end_date: Union[datetime, date] = None,
        text_lang: Optional[str] = 'en',
        entity_name: Optional[str] = 'All',
        term: Optional[str] = 'All',
        observer_type: Optional[str] = 'All',
        emotion: Optional[str] = 'All',
        user_info=Depends(get_current_user),
        handler=Depends(get_handler)):
    if not user_info:
        raise HTTPException(status_code=400, detail="User not found")

    return handler.get_word_cloud(FilterQueryParams(
        company_id=user_info.company_id,
        start_date=start_date,
        end_date=end_date,
        entity_name=entity_name,
        term=term,
        lang_code=text_lang,
        observer_type=observer_type,
        emotion=emotion
    ))


@routes.get("/dashboards", response_model=List[DashboardData])
def get_dashboard_data(
        user_info=Depends(get_current_user),
        handler=Depends(get_dashboard_service)):
    if not user_info:
        raise HTTPException(status_code=400, detail="User not found")

    return handler.get_dashboards()


@routes.get("/dashboards/panels", response_model=DashboardData)
def get_live_feed_dashboard_data(
        panel: str,
        user_info=Depends(get_current_user),
        handler=Depends(get_dashboard_service)):
    if not user_info:
        raise HTTPException(status_code=400, detail="User not found")

    return handler.get_dashboard_panel_data(panel)
