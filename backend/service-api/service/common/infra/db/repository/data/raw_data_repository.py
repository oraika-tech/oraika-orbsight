import logging
from datetime import datetime, timedelta
from typing import Any, List, Optional
from uuid import UUID

from sqlalchemy import UniqueConstraint, Column, DateTime
from sqlalchemy.dialects.postgresql import UUID as DB_UUID, JSONB
from sqlmodel import SQLModel, Field, select, Session

from service.common.infra.db.db_utils import get_tenant_engine

logger = logging.getLogger(__name__)


class RawDataEntity(SQLModel, table=True):
    __tablename__ = "insight_raw_data"
    __table_args__ = (UniqueConstraint('reference_id'),)

    identifier: Optional[int] = Field(default=None, primary_key=True)
    observer_id: UUID = Field(sa_column=Column(DB_UUID(as_uuid=True)))
    reference_id: str
    parent_reference_id: str
    raw_text: str
    unstructured_data: Optional[dict[str, Any]] = Field(default='{}', sa_column=Column(JSONB))
    event_time: datetime
    updated_at: Optional[datetime] = Field(sa_column=Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow))


def rotate_event_time(tenant_id: UUID, period_days: int):
    with Session(get_tenant_engine(tenant_id)) as session:
        items_to_update = session.exec(
            select(RawDataEntity)
            .where(RawDataEntity.event_time < datetime.now() - timedelta(days=period_days))
        ).all()

        logger.info("Items to update: %d", len(items_to_update))

        for item in items_to_update:
            item.event_time += timedelta(days=period_days)
            session.add(item)

        session.commit()


def insert_raw_data(tenant_id: UUID, raw_data_list: List[RawDataEntity]) -> List[RawDataEntity]:
    with Session(get_tenant_engine(tenant_id)) as session:
        success_raw_data_entity_list = []
        for raw_data_entity in raw_data_list:
            db_raw_data = session.exec(
                select(RawDataEntity)
                .where(RawDataEntity.reference_id == raw_data_entity.reference_id)
            ).first()

            if not db_raw_data:
                session.add(raw_data_entity)
                success_raw_data_entity_list.append(raw_data_entity)
            else:
                logger.debug("Found: %", str(db_raw_data))

        if success_raw_data_entity_list:
            session.commit()
            for success_raw_data_entity in success_raw_data_entity_list:
                session.refresh(success_raw_data_entity)

        return success_raw_data_entity_list
