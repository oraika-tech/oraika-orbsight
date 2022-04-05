from typing import Dict, List, Optional

from pydantic import BaseModel


class UnstructuredDataRequest(BaseModel):
    company_id: int
    raw_text: str


class StructuredData(BaseModel):
    entity_data: Dict[str, List[str]] = {}
    categories: Optional[List[str]] = None
    text_length: int
    emotion: Optional[str]
    remark: Optional[str] = None
    text_language: Optional[str]
