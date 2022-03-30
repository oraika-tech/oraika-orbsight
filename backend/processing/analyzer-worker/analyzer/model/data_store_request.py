from typing import Optional

from pydantic import BaseModel

from analyzer.model.structure_data_request import StructuredData


class ObserverInfo(BaseModel):
    identifier: int
    name: str
    type: str


class EntityInfo(BaseModel):
    identifier: int
    simple_name: str
    type: str
    country: Optional[str]
    city: Optional[str]


class DBStoreRequest(BaseModel):
    structured_data: StructuredData
    raw_data_identifier: int
    company_id: int
    observer_info: ObserverInfo
    entity_info: EntityInfo
