from enum import Enum
from typing import Optional, List

from pydantic import BaseModel


class ObserverType(int, Enum):
    Twitter = 1
    Android = 2
    iOS = 3


class ObserverJobEvent(BaseModel):
    company_id: int
    observer_identifier: int
    observer_name: str  # - app | twitter
    observer_type: ObserverType  # - app | twitter
    regulated_entity_type: Optional[List[str]]
    app_url: Optional[str]
    twitter_handle: Optional[str]
    lookup_period: Optional[str]
    limit_count: Optional[int]
    entity_identifier: int
    entity_simple_name: str
    regulated_type: Optional[List[str]]
    entity_country: Optional[str]
    entity_city: Optional[str]
