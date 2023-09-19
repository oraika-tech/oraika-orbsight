from datetime import datetime
from typing import List, Optional

from sqlalchemy import Column, Text, distinct, func, select
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.sql.operators import is_not
from sqlmodel import Field as SqlField
from sqlmodel import Session, SQLModel

from service.common.base_entity_manager import BaseEntityManager
from service.data.domain.base import BasePersistenceManager
from service.data.domain.model.filter_query_params import FilterQueryParams
from service.data.domain.model.text_analysis_data import TextAnalysisData


class ProcessedDataView(SQLModel, table=True):
    __tablename__ = "processed_data_view_v1"
    __table_args__ = {"schema": "data_view"}
    # __table_args__ = {'extend_existing': True}

    raw_data_id: int = SqlField(default=None, primary_key=True)
    processed_data_id: Optional[int]
    reference_id: Optional[str]
    conversation_id: Optional[str]
    event_time: Optional[datetime]

    emotion: Optional[str]
    rating: Optional[int]
    author_name: Optional[str]
    text_lang: Optional[str]
    text_hash: Optional[str]
    text_length: Optional[int]
    raw_text: Optional[str]
    url: Optional[str]

    entity_name: str
    observer_name: str
    observer_type: str

    taxonomy_tags: List[str] = SqlField(default='{}', sa_column=Column(ARRAY(Text)))
    taxonomy_terms: List[str] = SqlField(default='{}', sa_column=Column(ARRAY(Text)))
    categories: List[str] = SqlField(default='{}', sa_column=Column(ARRAY(Text)))

    def convert_to_model(self) -> TextAnalysisData:
        return TextAnalysisData(
            raw_data_id=self.raw_data_id,
            event_time=self.event_time,
            emotion=self.emotion,
            entity_name=self.entity_name,
            observer_type=self.observer_type,
            observer_name=self.observer_name,
            raw_text=self.raw_text,
            text_lang=self.text_lang,
            author_name=self.author_name,
            categories=self.categories or [],
            taxonomy_terms=self.taxonomy_terms,
            taxonomy_tags=self.taxonomy_tags,
        )


class DataDBManager(BasePersistenceManager, BaseEntityManager):

    @staticmethod
    def _get_updated_query_with_params(data, query, params: FilterQueryParams):

        if params.start_date:
            query = query.filter(data.event_time >= params.start_date)

        if params.end_date:
            query = query.filter(data.event_time <= params.end_date)

        if params.entity_name and params.entity_name != 'All':
            query = query.filter(data.entity_name == params.entity_name)

        if params.observer_type and params.observer_type != 'All':
            query = query.filter(data.observer_type == params.observer_type)

        if params.observer_name and params.observer_name != 'All':
            query = query.filter(data.observer_name == params.observer_name)

        if params.lang_code and params.lang_code != 'All':
            query = query.filter(data.text_lang == params.lang_code)

        if params.term and params.term != 'All':
            query = query.filter(data.taxonomy_terms.any(params.term))

        if params.tags and params.tags != 'All':
            query = query.filter(data.taxonomy_tags.any(params.tags))

        if params.emotion and params.emotion != 'All':
            query = query.filter(data.emotion == params.emotion)

        return query

    def get_text_analysis_data(self, params: FilterQueryParams) -> List[TextAnalysisData]:
        with Session(self._get_tenant_engine(params.tenant_id)) as session:
            query = session.query(ProcessedDataView)
            query = self._get_updated_query_with_params(ProcessedDataView, query, params)
            query = query.order_by(ProcessedDataView.event_time.desc())  # type: ignore
            if params.limit:
                query = query.limit(params.limit)
            result_set = query.all()
            if result_set:
                return [text_analysis_data.convert_to_model() for text_analysis_data in result_set]
            else:
                return []

    def get_distinct_terms(self, params: FilterQueryParams) -> List[str]:
        with Session(self._get_tenant_engine(params.tenant_id)) as session:
            query = select(func.unnest(ProcessedDataView.taxonomy_terms).label('taxonomy_value')) \
                .distinct() \
                .filter(ProcessedDataView.taxonomy_terms != None) \
                .order_by('taxonomy_value')
            query = self._get_updated_query_with_params(ProcessedDataView, query, params)
            return self._execute_query(session, query)

    def get_distinct_languages(self, params: FilterQueryParams) -> List[str]:
        with Session(self._get_tenant_engine(params.tenant_id)) as session:
            query = select(distinct(ProcessedDataView.text_lang)).filter(
                is_not(ProcessedDataView.text_lang, None)
            ).order_by(
                ProcessedDataView.text_lang
            )
            query = self._get_updated_query_with_params(ProcessedDataView, query, params)
            return self._execute_query(session, query)

    def get_distinct_entity_names(self, params: FilterQueryParams) -> List[str]:
        with Session(self._get_tenant_engine(params.tenant_id)) as session:
            query = select(distinct(ProcessedDataView.entity_name)).filter(
                is_not(ProcessedDataView.entity_name, None)
            ).order_by(
                ProcessedDataView.entity_name
            )
            query = self._get_updated_query_with_params(ProcessedDataView, query, params)
            return self._execute_query(session, query)

    def get_distinct_observer_types(self, params: FilterQueryParams) -> List[str]:
        with Session(self._get_tenant_engine(params.tenant_id)) as session:
            query = select(distinct(ProcessedDataView.observer_type)).filter(
                is_not(ProcessedDataView.observer_type, None)
            ).order_by(
                ProcessedDataView.observer_type
            )
            query = self._get_updated_query_with_params(ProcessedDataView, query, params)
            return self._execute_query(session, query)
