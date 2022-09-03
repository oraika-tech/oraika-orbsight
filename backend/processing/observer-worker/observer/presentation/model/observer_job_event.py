from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class ObserverType(int, Enum):
    Twitter = 1
    Android = 2
    iOS = 3


class ObserverJobEvent(BaseModel):
    tenant_id: UUID
    observer_identifier: str
    observer_type: ObserverType  # - app | twitter
    app_url: Optional[str]
    twitter_handle: Optional[str]
    lookup_period: Optional[str]
    limit_count: Optional[int]
