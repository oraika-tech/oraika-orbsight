from enum import Enum
from typing import Optional, List

from pydantic import BaseModel


class ObserverType(int, Enum):
    Twitter = 1
    Android = 2
    iOS = 3


class ObserverData(BaseModel):
    identifier: int
    name: str
    type: ObserverType
    regulated_entity_type: List[str]


class EntityData(BaseModel):
    identifier: int
    simple_name: str
    country: Optional[str]
    city: Optional[str]


class TextData(BaseModel):
    identifier: int
    raw_text: str
    event_time: str


class AnalyzerAPIRequest(BaseModel):
    company_id: int
    observer: ObserverData
    entity: EntityData
    text_data: TextData


class AnalyzerAPIResponse(BaseModel):
    identifier: int
