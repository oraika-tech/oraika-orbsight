from datetime import datetime
from typing import List, Tuple
from uuid import UUID

from sqlalchemy import and_, or_, Boolean
from sqlalchemy.engine import Row
from sqlalchemy.sql.operators import is_
from sqlmodel import Session, col, select, cast

from service.common.infra.db.db_utils import get_tenant_engine
from service.common.infra.db.repository.data.processed_data_repository import ProcessedDataEntity
from service.common.infra.db.repository.data.raw_data_repository import RawDataEntity
from service.common.infra.db.repository.workflow.node_meta_repository import WorkflowNodeMetaEntity


def get_unsent_processed_data(tenant_id: UUID, min_event_time: datetime) -> List[Tuple[RawDataEntity, ProcessedDataEntity]]:
    with (Session(get_tenant_engine(tenant_id)) as session):
        query = select(RawDataEntity, ProcessedDataEntity) \
            .join(ProcessedDataEntity, cast(RawDataEntity.identifier == ProcessedDataEntity.raw_data_id, Boolean)) \
            .join(WorkflowNodeMetaEntity, cast(RawDataEntity.identifier == WorkflowNodeMetaEntity.data_id, Boolean), isouter=True) \
            .where(
            and_(
                or_(
                    col(RawDataEntity.updated_at) > min_event_time,
                    col(ProcessedDataEntity.updated_at) > min_event_time,
                ),
                or_(
                    is_(col(WorkflowNodeMetaEntity.data_id), None),
                    col(WorkflowNodeMetaEntity.status).notin_(['SENT', 'FAILED']),
                    col(RawDataEntity.updated_at) > col(WorkflowNodeMetaEntity.updated_at),
                    col(ProcessedDataEntity.updated_at) > col(WorkflowNodeMetaEntity.updated_at)
                )
            )
        ).order_by(
            col(RawDataEntity.identifier),
            col(ProcessedDataEntity.updated_at).desc(),
            col(WorkflowNodeMetaEntity.identifier).desc()
        ).distinct(col(RawDataEntity.identifier))

        # Execution and Result Mapping
        results: list[Row] = list(session.execute(query).all())
        return [(raw_data, processed_data) for raw_data, processed_data in results]
