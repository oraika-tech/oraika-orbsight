from datetime import datetime
from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel
from sqlalchemy import Column, DateTime
from sqlmodel import SQLModel, Field, Session

from service.common.db.base_entity_manager import BaseEntityManager
from service.workflow.nodes.analyzer.domain_models import StructuredData


class DBStoreRequest(BaseModel):
    structured_data: StructuredData
    raw_data_identifier: int
    tenant_id: UUID


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
    # Text Features
    text_length: int
    text_lang: str
    # To store some comment or un categories info
    remark: str
    updated_at: Optional[datetime] = Field(sa_column=Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow))
    is_deleted: bool = Field(default=False)

    @staticmethod
    def convert_to_entity(data_request: DBStoreRequest):
        return ProcessedDataEntity(
            raw_data_id=data_request.raw_data_identifier,
            taxonomy_tags=data_request.structured_data.tags or [],
            taxonomy_terms=data_request.structured_data.terms or [],
            emotion=data_request.structured_data.emotion,
            categories=data_request.structured_data.categories or [],
            text_length=data_request.structured_data.text_length,
            text_lang=data_request.structured_data.text_language,
            remark=data_request.structured_data.remark,
        )


class ProcessedDataEntityManager(BaseEntityManager):

    def insert_structured_data(self, data_request: DBStoreRequest) -> int:
        data_entity = ProcessedDataEntity.convert_to_entity(data_request)
        with Session(self._get_tenant_engine(data_request.tenant_id)) as session:
            session.add(data_entity)
            session.commit()
            session.refresh(data_entity)
            return data_entity.identifier
