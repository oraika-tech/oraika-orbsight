import logging
from datetime import date, datetime
from typing import List, Optional, Union

from fastapi import APIRouter, Depends
from starlette.exceptions import HTTPException

from service.app.auth.domain.user_service import get_current_user
from service.app.data.data_models import TextAnalysisData, DataEntity, DataTerm
from service.app.data.data_service import (get_languages, get_data_entities, get_data_terms, get_data_sources_types,
                                           get_key_phrases, get_word_cloud, get_text_analysis_data)
from service.app.data.utils.key_phrases_utils import EmotionKeyPhrases
from service.app.data.utils.word_freq_utils import EmotionWordFrequency
from service.common.models import FilterQueryParams, DataSourceType

logger = logging.getLogger(__name__)

routes = APIRouter()


@routes.get("/text", response_model=List[TextAnalysisData])
def get_raw_and_processed(
        start_date: Optional[Union[datetime, date]] = None,
        end_date: Optional[Union[datetime, date]] = None,
        limit: Optional[int] = None,
        text_lang: Optional[str] = 'en',
        entity_name: Optional[str] = 'All',
        term: Optional[str] = 'All',
        observer_type: Optional[str] = 'All',
        emotion: Optional[str] = 'All',
        user_info=Depends(get_current_user)):
    if not user_info:
        raise HTTPException(status_code=400, detail="User not found")

    return get_text_analysis_data(FilterQueryParams(
        tenant_id=user_info.preferred_tenant_id,
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
        start_date: Optional[Union[datetime, date]] = None,
        end_date: Optional[Union[datetime, date]] = None,
        entity_name: Optional[str] = 'All',
        term: Optional[str] = 'All',
        observer_type: Optional[str] = 'All',
        emotion: Optional[str] = 'All',
        user_info=Depends(get_current_user)):
    return get_languages(FilterQueryParams(
        tenant_id=user_info.preferred_tenant_id,
        start_date=start_date,
        end_date=end_date,
        entity_name=entity_name,
        term=term,
        observer_type=observer_type,
        emotion=emotion
    ))


@routes.get("/entities", response_model=List[DataEntity], response_model_exclude_none=True)
def get_unique_entities_from_data(
        start_date: Optional[Union[datetime, date]] = None,
        end_date: Optional[Union[datetime, date]] = None,
        text_lang: Optional[str] = 'en',
        term: Optional[str] = 'All',
        observer_type: Optional[str] = None,
        emotion: Optional[str] = None,
        user_info=Depends(get_current_user)):
    return get_data_entities(FilterQueryParams(
        tenant_id=user_info.preferred_tenant_id,
        start_date=start_date,
        end_date=end_date,
        term=term,
        lang_code=text_lang,
        observer_type=observer_type,
        emotion=emotion
    ))


@routes.get("/terms", response_model=List[DataTerm], response_model_exclude_none=True)
def get_unique_terms_from_data(
        start_date: Optional[Union[datetime, date]] = None,
        end_date: Optional[Union[datetime, date]] = None,
        text_lang: Optional[str] = 'en',
        entity_name: Optional[str] = 'All',
        observer_type: Optional[str] = None,
        emotion: Optional[str] = None,
        user_info=Depends(get_current_user)):
    return get_data_terms(FilterQueryParams(
        tenant_id=user_info.preferred_tenant_id,
        start_date=start_date,
        end_date=end_date,
        entity_name=entity_name,
        lang_code=text_lang,
        observer_type=observer_type,
        emotion=emotion
    ))


@routes.get("/source-types", response_model=List[DataSourceType], response_model_exclude_none=True)
def get_data_sources_from_data(
        start_date: Optional[Union[datetime, date]] = None,
        end_date: Optional[Union[datetime, date]] = None,
        text_lang: Optional[str] = 'en',
        entity_name: Optional[str] = 'All',
        term: Optional[str] = 'All',
        emotion: Optional[str] = 'All',
        user_info=Depends(get_current_user)):
    return get_data_sources_types(FilterQueryParams(
        tenant_id=user_info.preferred_tenant_id,
        start_date=start_date,
        end_date=end_date,
        lang_code=text_lang,
        entity_name=entity_name,
        term=term,
        emotion=emotion
    ))


@routes.get("/key-phrases", response_model=List[EmotionKeyPhrases], response_model_exclude_none=True)
def get_key_phrases_from_data(
        start_date: Optional[Union[datetime, date]] = None,
        end_date: Optional[Union[datetime, date]] = None,
        text_lang: Optional[str] = 'en',
        entity_name: Optional[str] = 'All',
        term: Optional[str] = 'All',
        observer_type: Optional[str] = 'All',
        emotion: Optional[str] = 'All',
        limit: Optional[int] = None,
        user_info=Depends(get_current_user)):
    if not user_info:
        raise HTTPException(status_code=400, detail="User not found")

    return get_key_phrases(FilterQueryParams(
        tenant_id=user_info.preferred_tenant_id,
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
        start_date: Optional[Union[datetime, date]] = None,
        end_date: Optional[Union[datetime, date]] = None,
        text_lang: Optional[str] = 'en',
        entity_name: Optional[str] = 'All',
        term: Optional[str] = 'All',
        observer_type: Optional[str] = 'All',
        emotion: Optional[str] = 'All',
        user_info=Depends(get_current_user)):
    if not user_info:
        raise HTTPException(status_code=400, detail="User not found")

    return get_word_cloud(FilterQueryParams(
        tenant_id=user_info.preferred_tenant_id,
        start_date=start_date,
        end_date=end_date,
        entity_name=entity_name,
        term=term,
        lang_code=text_lang,
        observer_type=observer_type,
        emotion=emotion))
