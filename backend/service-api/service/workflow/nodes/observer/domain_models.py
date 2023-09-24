from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class ObserverType(int, Enum):
    Twitter = 1
    Android = 2
    iOS = 3
    GoogleMaps = 4
    Facebook = 5
    Reddit = 6
    GoogleNews = 7


class ObserverJobData(BaseModel):
    tenant_id: UUID
    observer_id: UUID
    observer_type: ObserverType  # - app | twitter
    url: Optional[str]
    query: Optional[str]
    country: Optional[str]
    language: Optional[str]
    page_id: Optional[str]
    subreddit: Optional[str]
    lookup_period: Optional[str]
    limit_count: Optional[int]
