from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID

from sqlalchemy import Column, Enum as SQLEnum, DateTime
from sqlalchemy import and_, or_, select, join
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql.operators import is_
from sqlmodel import Field, col
from sqlmodel import Session, SQLModel

from service.common.db.base_entity_manager import BaseEntityManager
from service.common.db.processed_data_entity_manager import ProcessedDataEntity
from service.common.db.raw_data_entity_manager import RawDataEntity
from service.workflow.nodes.spacepulse.spacepulse_client import SpacePulsePostRequest


class NodeMetaState(str, Enum):
    SENT = 'SENT'
    FAILED = 'FAILED'


class WorkflowNodeMetaEntity(SQLModel, table=True):
    __tablename__ = 'workflow_node_meta'
    identifier: Optional[int] = Field(default=None, primary_key=True)
    data_id: int
    status: NodeMetaState = Field(sa_column=Column(SQLEnum(NodeMetaState)))
    error_message: Optional[str]
    additional_data: Optional[dict] = Field(default='{}', sa_column=Column(JSONB))
    updated_at: Optional[datetime] = Field(sa_column=Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow))


class WorkflowNodeMetaEntityManager(BaseEntityManager):

    def get_unsent_processed_data(self, tenant_id: UUID, min_event_time: datetime):
        with Session(self._get_tenant_engine(tenant_id)) as session:
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
            results = session.execute(query).all()
            spacepulse_requests = [
                SpacePulsePostRequest(
                    id=raw_data.identifier,
                    text=raw_data.raw_text,
                    sentiment=processed_data.emotion,
                    departments=processed_data.taxonomy_tags,
                    activities=processed_data.taxonomy_terms,
                    source="Google Reviews",
                    link=raw_data.unstructured_data.get("review_link"),
                    rating=raw_data.unstructured_data.get("review_rating"),
                    timestamp=int(raw_data.event_time.timestamp()),
                    owner_answer_timestamp=raw_data.unstructured_data.get("owner_answer_timestamp"),
                    likes=raw_data.unstructured_data.get("review_likes")
                )
                for raw_data, processed_data in results
            ]

            return spacepulse_requests

    def update_status(self, tenant_id: UUID, raw_data_id: int, status: str):
        with Session(self._get_tenant_engine(tenant_id)) as session:
            record = session.query(WorkflowNodeMetaEntity).filter(
                WorkflowNodeMetaEntity.data_id == raw_data_id
            ).first()

            if record:
                # Update the existing record
                record.status = status
                record.error_message = None
            else:
                # Insert a new record
                new_record = WorkflowNodeMetaEntity(
                    data_id=raw_data_id,
                    status=status
                )
                session.add(new_record)

            session.commit()

    def log_error(self, tenant_id: UUID, raw_data_id: int, error_message: str):
        with Session(self._get_tenant_engine(tenant_id)) as session:
            record = session.query(WorkflowNodeMetaEntity).filter(
                WorkflowNodeMetaEntity.data_id == raw_data_id
            ).first()

            if record:
                # Update the existing record
                record.status = 'FAILED'
                record.error_message = error_message
            else:
                # Insert a new record
                new_record = WorkflowNodeMetaEntity(
                    data_id=raw_data_id,
                    status='FAILED',
                    error_message=error_message
                )
                session.add(new_record)

            session.commit()
