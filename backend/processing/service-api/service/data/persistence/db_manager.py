from datetime import datetime, date, time
from typing import Optional, Any, List, Union, Dict

from pydantic import Field
from sqlalchemy import Column, select, distinct
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import Field as SqlField, create_engine, Session, SQLModel

from service.data.domain.base import BasePersistenceManager

from service.data.domain.model.raw_data import RawDataInfo
from service.data.domain.model.processed_data import ProcessedDataInfo


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
        # self.engine = create_engine(connection_string, echo="debug")
        self.engine = create_engine(connection_string)

    def get_processed_data_with_raw_data(
            self,
            company_id: int,
            start_date: Union[datetime, date, time],
            end_date: Union[datetime, date, time],
            text_lang: str = 'en',
            entity_name: str = 'All',
            observer_type: str = 'All'
    ) -> Optional[List[ProcessedDataInfo]]:
        with Session(self.engine) as session:

            query = session.query(ProcessedData, RawData).filter(
                ProcessedData.is_deleted == False,
                ProcessedData.company_id == company_id,
                ProcessedData.raw_data_id == RawData.identifier,
                ProcessedData.text_lang == text_lang,
                ProcessedData.remark == None,
                ProcessedData.emotion != None,
                ProcessedData.event_time >= start_date,
                ProcessedData.event_time <= end_date,
            )

            if entity_name != 'All':
                query = query.filter(
                    ProcessedData.entity_name == entity_name
                )

            if observer_type != 'All':
                query = query.filter(
                    ProcessedData.observer_type == observer_type
                )

            result_set = query.all()

            if result_set is not None:
                return [
                    processed_data.convert_to_model(raw_data)
                    for processed_data, raw_data in result_set
                ]

    def get_distinct_entity_names(
            self, company_id: int
    ) -> Optional[List[str]]:
        with Session(self.engine) as session:
            stmt = select(distinct(ProcessedData.entity_name)).filter(
                ProcessedData.is_deleted == False,
                ProcessedData.company_id == company_id,
                ProcessedData.entity_name != None
            )
            row_list = session.exec(stmt)

            if row_list is not None:
                return [row[0] for row in row_list]

    def get_distinct_observer_types(
            self, company_id: int
    ) -> Optional[List[str]]:
        with Session(self.engine) as session:
            stmt = select(distinct(ProcessedData.observer_type)).filter(
                ProcessedData.is_deleted == False,
                ProcessedData.company_id == company_id,
                ProcessedData.observer_type != None
            )
            row_list = session.exec(stmt)

            if row_list is not None:
                return [row[0] for row in row_list]
