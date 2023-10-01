import logging
from datetime import datetime
from uuid import UUID

from sqlalchemy import and_
from sqlalchemy import false
from sqlalchemy import not_
from sqlalchemy.orm import Session
from sqlmodel import Session
from sqlmodel import col

from service.common.infra.db.db_utils import get_tenant_engine
from service.common.infra.db.repository.data.processed_data_repository import ProcessedDataEntity
from service.common.infra.db.repository.data.raw_data_repository import RawDataEntity

logger = logging.getLogger(__name__)


def get_unprocessed_data(tenant_id: UUID, min_event_time: datetime) -> list[RawDataEntity]:
    with Session(get_tenant_engine(tenant_id)) as session:
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
