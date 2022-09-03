from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class UnstructuredDataRequest(BaseModel):
    tenant_id: UUID
    raw_text: str


class StructuredData(BaseModel):
    tags: List[str] = Field([])
    terms: List[str] = Field([])
    categories: Optional[List[str]] = None
    text_length: int
    emotion: Optional[str]
    remark: Optional[str] = None
    text_language: Optional[str]
