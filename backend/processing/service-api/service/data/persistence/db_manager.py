from datetime import datetime
from typing import Optional, Any, List, Dict

from pydantic import Field
from sqlalchemy import Column, select, distinct
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import Field as SqlField, create_engine, Session, SQLModel

from service.data.domain.base import BasePersistenceManager
from service.data.domain.model.text_analysis_data import TextAnalysisData
from service.data.domain.model.filter_query_params import FilterQueryParams
from service.data.domain.model.processed_data import ProcessedDataInfo
from service.data.domain.model.raw_data import RawDataInfo


class RawData(SQLModel, table=True):
    __tablename__ = "raw_data"
    __table_args__ = {'extend_existing': True}

    identifier: Optional[int] = SqlField(default=None, primary_key=True)
    company_id: int
    observer_id: int
    observer_name: str
    observer_type: str
    entity_id: int
    entity_name: str
    regulated_entity_type: List[str]
    raw_text: str
    data: Optional[Dict[str, Any]] = SqlField(default='{}', sa_column=Column(JSONB))
    event_time: Optional[datetime]
    is_deleted: bool

    def convert_to_model(self) -> RawDataInfo:
        return RawDataInfo(
            identifier=self.identifier,
            observer_id=self.observer_id,
            observer_name=self.observer_name,
            observer_type=self.observer_type,
            entity_id=self.entity_id,
            entity_name=self.entity_name,
            regulated_entity_type=self.regulated_entity_type,
            raw_text=self.raw_text,
            data=self.data,
            event_time=self.event_time,
        )


class ProcessedData(SQLModel, table=True):
    __tablename__ = "processed_data"
    __table_args__ = {'extend_existing': True}

    identifier: Optional[int] = SqlField(default=None, primary_key=True)
    company_id: int
    raw_data_id: int
    event_time: Optional[datetime]
    emotion: Optional[str]
    fraud: Optional[bool]
    complaint: Optional[bool]
    harassment: Optional[bool]
    access: Optional[bool]
    delay: Optional[bool]
    interface: Optional[bool]
    charges: Optional[bool]
    text_lang: Optional[str]
    entity_name: str
    regulated_entity_type: List[str]
    observer_name: str
    observer_type: str
    remark: Optional[str]
    is_deleted: bool

    def convert_to_model(self, raw_data: Optional[RawData] = None) -> ProcessedDataInfo:
        return ProcessedDataInfo(
            identifier=self.identifier,
            raw_data_id=self.raw_data_id,
            event_time=self.event_time,
            emotion=self.emotion,
            fraud=self.fraud,
            complaint=self.complaint,
            harassment=self.harassment,
            access=self.access,
            delay=self.delay,
            interface=self.interface,
            charges=self.charges,
            text_lang=self.text_lang,
            entity_name=self.entity_name,
            regulated_entity_type=self.regulated_entity_type,
            observer_name=self.observer_name,
            observer_type=self.observer_type,
            raw_data=None if raw_data is None else raw_data.convert_to_model(),
        )


class TextAnalysisDataEntity(SQLModel, table=True):
    __tablename__ = "processed_data_view_v1"
    __table_args__ = {'extend_existing': True}

    raw_data_id: Optional[int] = SqlField(default=None, primary_key=True)
    processed_data_id: Optional[int]
    reference_id: Optional[int]
    conversation_id: Optional[int]
    company_id: Optional[int]
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
    regulated_entity_type: List[str]
    observer_type: str

    taxonomy_fields: List[str]
    taxonomy_values: List[str]
    categories: List[str]

    def convert_to_model(self) -> TextAnalysisData:
        return TextAnalysisData(
            raw_data_id=self.raw_data_id,
            event_time=self.event_time,
            emotion=self.emotion,
            entity_name=self.entity_name,
            observer_type=self.observer_type,
            raw_text=self.raw_text,
            text_lang=self.text_lang,
            author_name=self.author_name,
            categories=self.categories,
            taxonomies=self.taxonomy_values
        )


class DataDBManager(BasePersistenceManager):
    db_host: Optional[str] = Field("localhost:5432", env='DB_HOST')
    db_name: str = Field("obsights_rbi", env='DATA_DB_NAME')
    db_user: str = Field("postgres", env='DATA_DB_USER')
    db_password: str = Field("studio", env='DATA_DB_PASSWORD')
    db_engine_name: str = Field("postgresql", env="DB_ENGINE_NAME")
    engine: Any

    def __init__(self, **values: Any):
        super().__init__(**values)
        connection_string = f"{self.db_engine_name}://{self.db_user}:{self.db_password}@{self.db_host}/{self.db_name}"
        self.engine = create_engine(connection_string)

    @staticmethod
    def _get_updated_query_with_params(entity, query, params: FilterQueryParams):

        query = query.filter(entity.company_id == params.company_id)

        if params.start_date:
            query = query.filter(entity.event_time >= params.start_date)

        if params.end_date:
            query = query.filter(entity.event_time <= params.end_date)

        if params.entity_name and params.entity_name != 'All':
            query = query.filter(entity.entity_name == params.entity_name)

        if params.observer_type and params.observer_type != 'All':
            query = query.filter(entity.observer_type == params.observer_type)

        if params.lang_code and params.lang_code != 'All':
            query = query.filter(entity.text_lang == params.lang_code)

        if params.emotion and params.emotion != 'All':
            query = query.filter(entity.emotion == params.emotion)
        else:
            query = query.filter(entity.emotion != None)

        return query

    @staticmethod
    def _execute_query(session, query):
        row_list = session.exec(query)
        if row_list is not None:
            return [row[0] for row in row_list]
        else:
            return []

    def get_text_analysis_data(self, params: FilterQueryParams) -> Optional[List[TextAnalysisData]]:
        with Session(self.engine) as session:
            query = session.query(TextAnalysisDataEntity)
            query = self._get_updated_query_with_params(TextAnalysisDataEntity, query, params)
            query = query.order_by(TextAnalysisDataEntity.event_time.desc())
            if params.limit:
                query = query.limit(params.limit)
            result_set = query.all()
            if result_set is not None:
                return [text_analysis_data.convert_to_model() for text_analysis_data in result_set]
            else:
                return []

    def get_distinct_languages(self, params: FilterQueryParams) -> Optional[List[str]]:
        with Session(self.engine) as session:
            query = select(distinct(ProcessedData.text_lang)).filter(
                ProcessedData.is_deleted == False,
                ProcessedData.text_lang != None
            ).order_by(
                ProcessedData.text_lang
            )
            query = self._get_updated_query_with_params(ProcessedData, query, params)
            return self._execute_query(session, query)

    def get_distinct_entity_names(self, params: FilterQueryParams) -> Optional[List[str]]:
        with Session(self.engine) as session:
            query = select(distinct(ProcessedData.entity_name)).filter(
                ProcessedData.is_deleted == False,
                ProcessedData.entity_name != None
            ).order_by(
                ProcessedData.entity_name
            )
            query = self._get_updated_query_with_params(ProcessedData, query, params)
            query = query.order_by(ProcessedData.entity_name)
            return self._execute_query(session, query)

    def get_distinct_observer_types(self, params: FilterQueryParams) -> Optional[List[str]]:
        with Session(self.engine) as session:
            query = select(distinct(ProcessedData.observer_type)).filter(
                ProcessedData.is_deleted == False,
                ProcessedData.observer_type != None
            ).order_by(
                ProcessedData.observer_type
            )
            query = self._get_updated_query_with_params(ProcessedData, query, params)
            return self._execute_query(session, query)
