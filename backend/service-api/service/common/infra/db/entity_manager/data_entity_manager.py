import logging
from datetime import datetime
from uuid import UUID

from sqlalchemy import and_
from sqlalchemy import false
from sqlalchemy import not_
from sqlalchemy.orm import Session
from sqlalchemy.sql.operators import is_
from sqlmodel import Session
from sqlmodel import col

from service.common.infra.db.db_utils import get_tenant_engine
from service.common.infra.db.repository.data.processed_data_repository import ProcessedDataEntity
from service.common.infra.db.repository.data.raw_data_repository import RawDataEntity

logger = logging.getLogger(__name__)


# To be used by analyzer workflow to fetch unprocessed data
def get_unprocessed_data(tenant_id: UUID, min_event_time: datetime, limit_count: int) -> list[RawDataEntity]:
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
        if limit_count > 0:
            query = query.limit(limit_count)
        return query.all()


# To be used by ner workflow to fetch unprocessed data
def get_unprocessed_people_data(tenant_id: UUID, min_event_time: datetime, limit_count: int = 0) -> list[RawDataEntity]:
    with Session(get_tenant_engine(tenant_id)) as session:
        subquery = session.query(ProcessedDataEntity.raw_data_id) \
            .filter(ProcessedDataEntity.is_deleted == false(),
                    is_(ProcessedDataEntity.people, None))

        query = session.query(RawDataEntity) \
            .filter(
            and_(
                RawDataEntity.event_time > min_event_time,
                col(RawDataEntity.identifier).in_(subquery)
            )
        )
        if limit_count > 0:
            query = query.limit(limit_count)
        return query.all()


# To be used by ner workflow to add people data
def update_people_data(tenant_id: UUID, people_list: list[dict]):
    with Session(get_tenant_engine(tenant_id)) as session:
        for people in people_list:
            # Search for the record with the given raw_data_id
            existing_record = session.query(ProcessedDataEntity).filter(
                and_(
                    ProcessedDataEntity.raw_data_id == people['raw_data_id'],
                    ProcessedDataEntity.is_deleted == false()
                )
            ).first()

            # If the record exists, update the people field
            if existing_record:
                existing_record.people = people['people']

        # Commit changes to the database
        session.commit()
