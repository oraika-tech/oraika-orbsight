from typing import List, Optional

from pydantic import BaseModel, Field


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
