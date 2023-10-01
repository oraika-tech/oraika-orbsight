from datetime import datetime
from typing import List, Tuple
from uuid import UUID

from sqlalchemy import select, join, and_, or_
from sqlalchemy.sql.operators import is_
from sqlmodel import Session, col

from service.common.infra.db.db_utils import get_tenant_engine
from service.common.infra.db.repository.data.processed_data_repository import ProcessedDataEntity
from service.common.infra.db.repository.data.raw_data_repository import RawDataEntity
from service.common.infra.db.repository.workflow.node_meta_repository import WorkflowNodeMetaEntity


def get_unsent_processed_data(tenant_id: UUID, min_event_time: datetime) -> List[Tuple[RawDataEntity, ProcessedDataEntity]]:
    with Session(get_tenant_engine(tenant_id)) as session:
        query = select([RawDataEntity, ProcessedDataEntity]).select_from(
            join(
                join(RawDataEntity, ProcessedDataEntity,
                     RawDataEntity.identifier == ProcessedDataEntity.raw_data_id),
                WorkflowNodeMetaEntity,
                RawDataEntity.identifier == WorkflowNodeMetaEntity.data_id,
                isouter=True
            )
        ).where(
            and_(
                or_(
                    col(RawDataEntity.updated_at) > min_event_time,
                    col(ProcessedDataEntity.updated_at) > min_event_time,
                ),
                or_(
                    is_(WorkflowNodeMetaEntity.data_id, None),
                    col(WorkflowNodeMetaEntity.status).notin_(['SENT', 'FAILED']),
                    col(RawDataEntity.updated_at) > col(WorkflowNodeMetaEntity.updated_at),
                    col(ProcessedDataEntity.updated_at) > col(WorkflowNodeMetaEntity.updated_at)
                )
            )
        ).order_by(
            RawDataEntity.identifier,
            col(ProcessedDataEntity.updated_at).desc(),
            col(WorkflowNodeMetaEntity.identifier).desc()
        ).distinct(RawDataEntity.identifier)

        # Execution and Result Mapping
        return session.execute(query).all()
