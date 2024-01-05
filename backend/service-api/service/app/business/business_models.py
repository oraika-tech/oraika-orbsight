from typing import Optional, List
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
    official_handle: Optional[str] = None
    url: Optional[str] = None


class ObserverInfo(BaseModel):
    identifier: Optional[UUID] = None
    name: str
    type: str
    entity_id: UUID
    entity_name: str
    config_data: ObserverData
    is_enabled: bool


class CategoryInfo(BaseModel):
    identifier: Optional[UUID] = None
    name: str
    is_enabled: bool


class DashboardData(BaseModel):
    title: str
    link: str


class EntityInfo(BaseModel):
    identifier: Optional[UUID] = None
    name: str
    tags: Optional[List[str]] = None
    is_enabled: bool


class StatsInfo(BaseModel):
    name: str
    value: Optional[int] = None


class TaxonomyInfo(BaseModel):
    identifier: Optional[UUID] = None
    keyword: str
    term: str
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    is_enabled: bool
