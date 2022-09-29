from typing import Optional
from uuid import UUID

from pydantic import BaseModel

OBSERVER_TYPE = {
    1: "Twitter",
    2: "Android",
    3: "iOS",
    4: "GoogleMaps",
    5: "Facebook",
    6: "Reddit",
    7: "GoogleNews"
}


class ObserverData(BaseModel):
    official_handle: Optional[str]
    url: Optional[str]


class ObserverInfo(BaseModel):
    identifier: Optional[UUID]
    name: str
    type: str
    entity_id: UUID
    entity_name: str
    config_data: ObserverData
    is_enabled: bool
