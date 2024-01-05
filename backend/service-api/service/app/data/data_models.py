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
    id: Optional[int] = None
    name: str


class DataTerm(BaseModel):
    name: str


class TextAnalysisData(BaseModel):
    raw_data_id: int
    event_time: Optional[datetime] = None
    emotion: Optional[str] = None
    entity_name: str
    observer_name: str
    observer_type: str
    raw_text: str
    text_lang: Optional[str] = None
    author_name: Optional[str] = None
    categories: List[str]
    taxonomy_tags: List[str]
    taxonomy_terms: List[str]


class RawData(BaseModel):
    identifier: Optional[int] = None
    observer_id: UUID
    reference_id: str
    parent_reference_id: Optional[str] = None
    raw_text: str
    unstructured_data: Optional[Dict[str, Any]] = None
    event_time: datetime


class TextAnalysisUpdateData(BaseModel):
    sentiment: Optional[str] = None
    departments: Optional[List[str]] = None
    activities: Optional[List[str]] = None
    people: Optional[List[str]] = None

    class Config:
        extra = "forbid"


class AnalysisData(BaseModel):
    id: int
    text: str
    source: str
    link: Optional[str] = None
    sentiment: str
    departments: list[str]
    activities: list[str]
    people: list[str]
    rating: Optional[int] = None
    timestamp: int
    owner_answer_timestamp: Optional[int] = None
    likes: Optional[int] = None
