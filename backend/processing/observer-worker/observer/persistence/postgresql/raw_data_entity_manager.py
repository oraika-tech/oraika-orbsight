import copy
import logging
from datetime import datetime
from typing import Optional, List, Any, Dict

from pydantic import BaseSettings, Field
from sqlalchemy import UniqueConstraint, Column
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import Field as SqlField, Session, SQLModel, create_engine

from analyzer.model.api_request_response import ObserverType
from observer.domain.raw_data import RawData

logger = logging.getLogger(__name__)


class RawDataEntity(SQLModel, table=True):
    __tablename__ = "raw_data"
    __table_args__ = (UniqueConstraint('reference_id'),)
    identifier: Optional[int] = SqlField(default=None, primary_key=True)
    company_id: int
    observer_id: int
    observer_name: str
    observer_type: str
    entity_id: int
    entity_name: str
    regulated_entity_type: List[str]
    reference_id: str
    parent_reference_id: str
    processing_status: str
    tags: Optional[Dict[str, str]]
    raw_text: str
    data: Optional[dict] = SqlField(default='{}', sa_column=Column(JSONB))
    event_time: datetime


class RawDataEntityManager(BaseSettings):
    db_host: Optional[str] = Field("localhost:5432", env='DB_HOST')
    db_name: str = Field("obsights_rbi", env='DB_NAME')
    db_user: str = Field("obsights", env='DB_USER')
    db_password: str = Field("obsights", env='DB_PASSWORD')
    engine: Any

    def __init__(self, **values: Any):
        super().__init__(**values)
        connection_string = f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}/{self.db_name}"
        self.engine = create_engine(connection_string)

    def insert_raw_data(self, raw_data_list: List[RawData]):
        with Session(self.engine) as session:
            success_raw_data_entity_list = []
            for raw_data in raw_data_list:
                db_raw_data = session.query(RawDataEntity) \
                    .filter(RawDataEntity.reference_id == raw_data.reference_id) \
                    .first()
                if not db_raw_data:
                    raw_data_entity = self.convert_to_entity(raw_data)
                    session.add(raw_data_entity)
                    success_raw_data_entity_list.append(raw_data_entity)
                else:
                    logger.debug("Found: %", str(db_raw_data))

            if success_raw_data_entity_list:
                session.commit()

            success_raw_data_list = []
            for raw_data_entity in success_raw_data_entity_list:
                if not raw_data_entity.identifier:
                    session.refresh(raw_data_entity)
                success_raw_data_list.append(self.convert_from_entity(raw_data_entity))

        return success_raw_data_list

    def convert_to_entity(self, raw_data: RawData):
        return RawDataEntity(
            company_id=raw_data.company_id,
            observer_id=raw_data.observer_id,
            observer_name=raw_data.observer_name,
            observer_type=raw_data.observer_type.name,
            entity_id=raw_data.entity_id,
            entity_name=raw_data.entity_name,
            regulated_entity_type=raw_data.regulated_entity_type,
            reference_id=raw_data.reference_id,
            parent_reference_id=raw_data.parent_reference_id,
            raw_text=raw_data.raw_text,
            # data=json.dumps(raw_data.data, default=datetime_handler),
            data=self.recursive_serialize(raw_data.data),
            event_time=raw_data.event_time
        )

    @staticmethod
    def convert_from_entity(raw_data_entity: RawDataEntity):
        return RawData(
            identifier=raw_data_entity.identifier,
            company_id=raw_data_entity.company_id,
            observer_id=raw_data_entity.observer_id,
            observer_name=raw_data_entity.observer_name,
            observer_type=ObserverType[raw_data_entity.observer_type],
            entity_id=raw_data_entity.entity_id,
            entity_name=raw_data_entity.entity_name,
            regulated_entity_type=raw_data_entity.regulated_entity_type,
            reference_id=raw_data_entity.reference_id,
            parent_reference_id=raw_data_entity.parent_reference_id,
            tags=raw_data_entity.tags,
            raw_text=raw_data_entity.raw_text,
            data=raw_data_entity.data,
            event_time=raw_data_entity.event_time
        )

    def recursive_serialize(self, original_data: Dict[str, Any]) -> dict:
        data = copy.deepcopy(original_data)

        for key, value in data.items():
            if isinstance(value, datetime):
                data[key] = value.isoformat()
            elif isinstance(value, Dict):
                self.recursive_serialize(value)

        return data
