from datetime import datetime
from typing import Optional, List, Sequence

from sqlalchemy import Column, Text, func, distinct
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.sql.operators import is_, is_not
from sqlmodel import SQLModel, Field, Session, any_, select, col

from service.common.infra.db.db_utils import get_tenant_engine
from service.common.models import FilterQueryParams


class ProcessedDataView(SQLModel, table=True):
    __tablename__ = "processed_data_view_v1"
    __table_args__ = {"schema": "data_view"}
    # __table_args__ = {'extend_existing': True}

    raw_data_id: int = Field(default=None, primary_key=True)
    processed_data_id: Optional[int] = None
    reference_id: Optional[str] = None
    conversation_id: Optional[str] = None
    event_time: Optional[datetime] = None

    emotion: Optional[str] = None
    rating: Optional[int] = None
    author_name: Optional[str] = None
    text_lang: Optional[str] = None
    text_hash: Optional[str] = None
    text_length: Optional[int] = None
    raw_text: Optional[str] = None
    url: Optional[str] = None

    entity_name: str
    observer_name: str
    observer_type: str

    taxonomy_tags: List[str] = Field(default='{}', sa_column=Column(ARRAY(Text)))
    taxonomy_terms: List[str] = Field(default='{}', sa_column=Column(ARRAY(Text)))
    categories: List[str] = Field(default='{}', sa_column=Column(ARRAY(Text)))
    people: List[str] = Field(default='{}', sa_column=Column(ARRAY(Text)))


def _get_updated_query_with_params(data, query, params: FilterQueryParams):
    if params.start_date:
        query = query.where(data.event_time >= params.start_date)

    if params.end_date:
        query = query.where(data.event_time <= params.end_date)

    if params.entity_name and params.entity_name != 'All':
        query = query.where(data.entity_name == params.entity_name)

    if params.observer_type and params.observer_type != 'All':
        query = query.where(data.observer_type == params.observer_type)

    if params.observer_name and params.observer_name != 'All':
        query = query.where(data.observer_name == params.observer_name)

    if params.lang_code and params.lang_code != 'All':
        query = query.where(data.text_lang == params.lang_code)

    if params.term and params.term != 'All':
        query = query.where(any_(data.taxonomy_terms) == params.term)

    if params.tags and params.tags != 'All':
        query = query.where(any_(data.taxonomy_tags) == params.tags)

    if params.emotion and params.emotion != 'All':
        query = query.where(data.emotion == params.emotion)

    if params.raw_data_id is not None:
        query = query.where(data.raw_data_id == params.raw_data_id)

    return query


def _list(results: Sequence) -> list:
    return [result for result in results if result]


def get_processed_data_view(params: FilterQueryParams) -> List[ProcessedDataView]:
    with Session(get_tenant_engine(params.tenant_id)) as session:
        query = select(ProcessedDataView)
        query = _get_updated_query_with_params(ProcessedDataView, query, params)
        query = query.order_by(ProcessedDataView.event_time.desc())  # type: ignore
        if params.limit:
            query = query.limit(params.limit)
        return _list(session.exec(query).all())


def get_distinct_terms(params: FilterQueryParams) -> List[str]:
    with Session(get_tenant_engine(params.tenant_id)) as session:
        query = select(func.unnest(ProcessedDataView.taxonomy_terms).label('taxonomy_value')) \
            .distinct() \
            .where(is_(col(ProcessedDataView.taxonomy_terms), None)) \
            .order_by('taxonomy_value')
        query = _get_updated_query_with_params(ProcessedDataView, query, params)
        return _list(session.exec(query).all())


def get_distinct_languages(params: FilterQueryParams) -> List[str]:
    with (Session(get_tenant_engine(params.tenant_id)) as session):
        query = select(distinct(col(ProcessedDataView.text_lang))) \
            .where(is_not(col(ProcessedDataView.text_lang), None)) \
            .order_by(ProcessedDataView.text_lang)
        query = _get_updated_query_with_params(ProcessedDataView, query, params)
        return _list(session.exec(query).all())


def get_distinct_entity_names(params: FilterQueryParams) -> List[str]:
    with Session(get_tenant_engine(params.tenant_id)) as session:
        query = select(distinct(col(ProcessedDataView.entity_name))) \
            .where(is_not(col(ProcessedDataView.entity_name), None)) \
            .order_by(ProcessedDataView.entity_name)
        query = _get_updated_query_with_params(ProcessedDataView, query, params)
        return _list(session.exec(query).all())


def get_distinct_observer_types(params: FilterQueryParams) -> List[str]:
    with Session(get_tenant_engine(params.tenant_id)) as session:
        query = select(distinct(col(ProcessedDataView.observer_type))) \
            .where(is_not(col(ProcessedDataView.observer_type), None)) \
            .order_by(ProcessedDataView.observer_type)
        query = _get_updated_query_with_params(ProcessedDataView, query, params)
        return _list(session.exec(query).all())
