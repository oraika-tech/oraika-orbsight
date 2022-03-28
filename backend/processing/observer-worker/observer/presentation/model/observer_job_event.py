from enum import Enum
from typing import Optional

from pydantic import BaseModel


class ObserverType(int, Enum):
    twitter = 1
    android = 2
    ios = 3


class ObserverJobEvent(BaseModel):
    company_id: int
    observer_identifier: int
    observer_type: ObserverType  # - app | twitter
    observer_name: str  # - app | twitter
    app_url: Optional[str]
    twitter_handle: Optional[str]
    lookup_period: Optional[str]
    limit_count: Optional[int]
    entity_identifier: int
    entity_simple_name: str
    entity_type: Optional[str]
    entity_country: Optional[str]
    entity_city: Optional[str]
