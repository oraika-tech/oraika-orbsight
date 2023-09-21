import copy
import logging
from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel
from sqlalchemy import Column, UniqueConstraint, false
from sqlalchemy import not_, and_
from sqlalchemy.dialects.postgresql import JSONB, UUID as DB_UUID
from sqlalchemy.orm import Session
from sqlmodel import Field as SqlField, col
from sqlmodel import Session, SQLModel

from service.common.db.base_entity_manager import BaseEntityManager
from service.common.db.processed_data_entity_manager import ProcessedDataEntity

logger = logging.getLogger(__name__)


class RawData(BaseModel):
    identifier: Optional[int]
    observer_id: UUID
    reference_id: str
    parent_reference_id: Optional[str]
    raw_text: str
    unstructured_data: Optional[Dict[str, Any]]
    event_time: datetime


class RawDataEntity(SQLModel, table=True):
    __tablename__ = "insight_raw_data"
    __table_args__ = (UniqueConstraint('reference_id'),)

    identifier: Optional[int] = SqlField(default=None, primary_key=True)
    observer_id: UUID = SqlField(sa_column=Column(DB_UUID(as_uuid=True)))
    reference_id: str
    parent_reference_id: str
    raw_text: str
    unstructured_data: Optional[dict] = SqlField(default='{}', sa_column=Column(JSONB))
    event_time: datetime


class RawDataEntityManager(BaseEntityManager):

    def insert_raw_data(self, tenant_id: UUID, raw_data_list: List[RawData]):
        with Session(self._get_tenant_engine(tenant_id)) as session:
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
        unstructured_data = self.recursive_serialize(raw_data.unstructured_data) \
            if raw_data.unstructured_data else None
        return RawDataEntity(
            observer_id=raw_data.observer_id,
            reference_id=raw_data.reference_id,
            parent_reference_id=raw_data.parent_reference_id,
            raw_text=raw_data.raw_text,
            # data=json.dumps(raw_data.data, default=datetime_handler),
            unstructured_data=unstructured_data,
            event_time=raw_data.event_time
        )

    @staticmethod
    def convert_from_entity(raw_data_entity: RawDataEntity):
        return RawData(
            identifier=raw_data_entity.identifier,
            observer_id=raw_data_entity.observer_id,
            reference_id=raw_data_entity.reference_id,
            parent_reference_id=raw_data_entity.parent_reference_id,
            raw_text=raw_data_entity.raw_text,
            unstructured_data=raw_data_entity.unstructured_data,
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

    def get_unprocessed_data(self, tenant_id: UUID, min_event_time: datetime):
        with Session(self._get_tenant_engine(tenant_id)) as session:
            subquery = session.query(ProcessedDataEntity.raw_data_id) \
                .filter(ProcessedDataEntity.is_deleted == false())

            query = session.query(RawDataEntity) \
                .filter(
                and_(
                    RawDataEntity.event_time > min_event_time,
                    not_(col(RawDataEntity.identifier).in_(subquery))
                )
            )
            return query.all()
