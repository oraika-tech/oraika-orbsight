from typing import Optional, Dict, List, Set
from uuid import UUID

from pydantic import BaseModel, Field


class AnalyzerJobRequest(BaseModel):
    tenant_id: UUID
    raw_data_id: int
    raw_text: str
    message: Optional[Dict]


class UnstructuredDataRequest(BaseModel):
    raw_data_id: int
    raw_text: str


class StructuredData(BaseModel):
    raw_data_id: int
    tags: List[str] = Field([])
    terms: List[str] = Field([])
    categories: Optional[List[str]] = None
    text_length: int
    emotion: Optional[str]
    remark: Optional[str] = None
    text_language: Optional[str]


class TaxonomyData(BaseModel):
    tags: Set[str] = Field(set())
    terms: Set[str] = Field(set())
