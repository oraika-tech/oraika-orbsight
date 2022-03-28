import json
import logging
from typing import Optional, List, Any, Dict

from obsei.misc.utils import datetime_handler
from pydantic import BaseSettings, Field
from sqlalchemy import UniqueConstraint, Column
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import Field as SqlField, Session, SQLModel, create_engine

from observer.domain.raw_data import RawData

logger = logging.getLogger(__name__)


class RawDataEntity(SQLModel, table=True):
    __tablename__ = "raw_data"
    __table_args__ = (UniqueConstraint('reference_id'),)
    identifier: Optional[int] = SqlField(default=None, primary_key=True)
    company_id: int
    observer_id: int
    reference_id: str
    parent_reference_id: str
    processing_status: str
    tags: Optional[Dict[str, str]]
    raw_text: str
    data: str = SqlField(default='{}', sa_column=Column(JSONB))


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

    @staticmethod
    def convert_to_entity(raw_data: RawData):
        return RawDataEntity(
            company_id=raw_data.company_id,
            observer_id=raw_data.observer_id,
            reference_id=raw_data.reference_id,
            parent_reference_id=raw_data.parent_reference_id,
            # tags=raw_data.tags,
            raw_text=raw_data.raw_text,
            data=json.dumps(raw_data.data, default=datetime_handler)
        )

    @staticmethod
    def convert_from_entity(raw_data_entity: RawDataEntity):
        return RawData(
            identifier=raw_data_entity.identifier,
            company_id=raw_data_entity.company_id,
            observer_id=raw_data_entity.observer_id,
            reference_id=raw_data_entity.reference_id,
            parent_reference_id=raw_data_entity.parent_reference_id,
            tags=raw_data_entity.tags,
            raw_text=raw_data_entity.raw_text,
            data=json.loads(raw_data_entity.data)
        )
