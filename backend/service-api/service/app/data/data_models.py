from datetime import datetime
from typing import Optional, List, Dict, Any
from uuid import UUID

from pydantic import BaseModel

LANG_CODE_TO_NAME = {
    "en": "English",
    "hi": "Hindi",
    "ta": "Tamil",
    "te": "Telugu",
    "gu": "Gujarati",
    "kn": "Kannada",
    "bn": "Bengali",
    "mr": "Marathi",
    "ml": "Malayalam",
    "pa": "Punjabi",
    "ur": "Urdu"
}


class DataEntity(BaseModel):
    id: Optional[int]
    name: str


class DataTerm(BaseModel):
    name: str


class TextAnalysisData(BaseModel):
    raw_data_id: int
    event_time: Optional[datetime]
    emotion: Optional[str]
    entity_name: str
    observer_name: str
    observer_type: str
    raw_text: str
    text_lang: Optional[str]
    author_name: Optional[str]
    categories: List[str]
    taxonomy_tags: List[str]
    taxonomy_terms: List[str]


class RawData(BaseModel):
    identifier: Optional[int]
    observer_id: UUID
    reference_id: str
    parent_reference_id: Optional[str]
    raw_text: str
    unstructured_data: Optional[Dict[str, Any]]
    event_time: datetime
