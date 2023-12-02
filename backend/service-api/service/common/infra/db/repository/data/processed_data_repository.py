from datetime import datetime
from typing import Optional, List
from uuid import UUID

from sqlalchemy import Column, DateTime, update
from sqlmodel import SQLModel, Field, Session

from service.common.infra.db.db_utils import get_tenant_engine


class ProcessedDataEntity(SQLModel, table=True):
    __tablename__ = "insight_processed_data"

    identifier: Optional[int] = Field(default=None, primary_key=True)
    raw_data_id: int
    # Extraction from Text
    taxonomy_tags: List[str]
    taxonomy_terms: List[str]
    # Extraction from AI model
    emotion: str
    categories: List[str]
    people: Optional[List[str]]
    # Text Features
    text_length: int
    text_lang: str
    # To store some comment or un categories info
    remark: str
    updated_at: Optional[datetime] = Field(sa_column=Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow))
    is_deleted: bool = Field(default=False)


def insert_structured_data(tenant_id: UUID, data_entity: ProcessedDataEntity) -> Optional[int]:
    with Session(get_tenant_engine(tenant_id)) as session:
        session.add(data_entity)
        session.commit()
        session.refresh(data_entity)
        return data_entity.identifier


def update_structured_data(tenant_id: UUID, update_processed_data: dict) -> int:
    with Session(get_tenant_engine(tenant_id)) as session:
        statement = update(ProcessedDataEntity) \
            .where(ProcessedDataEntity.raw_data_id == update_processed_data['raw_data_id']) \
            .values(**update_processed_data)

        result = session.execute(statement)
        session.commit()
        return result.rowcount  # type: ignore
