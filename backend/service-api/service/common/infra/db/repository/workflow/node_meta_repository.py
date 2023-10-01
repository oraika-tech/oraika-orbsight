from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlalchemy import Column, DateTime, Enum as SqlEnum
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import Session, Field, SQLModel

from service.common.infra.db.db_utils import get_tenant_engine
from service.common.models import NodeMetaState


class WorkflowNodeMetaEntity(SQLModel, table=True):
    __tablename__ = 'workflow_node_meta'
    identifier: Optional[int] = Field(default=None, primary_key=True)
    data_id: int
    status: NodeMetaState = Field(sa_column=Column(SqlEnum(NodeMetaState)))
    error_message: Optional[str]
    additional_data: Optional[dict] = Field(default='{}', sa_column=Column(JSONB))
    updated_at: Optional[datetime] = Field(sa_column=Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow))


def update_status(tenant_id: UUID, raw_data_id: int, status: str):
    with Session(get_tenant_engine(tenant_id)) as session:
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


def log_wf_error(tenant_id: UUID, raw_data_id: int, error_message: str):
    with Session(get_tenant_engine(tenant_id)) as session:
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
