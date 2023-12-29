from datetime import datetime
from typing import Optional
from typing import Type
from uuid import UUID

from pydantic import BaseModel

from service.common.models import TableName


class EntityInfo(BaseModel):
    identifier: Optional[UUID]
    name: str
    tags: Optional[list[str]]
    is_enabled: bool
    created_at: datetime
    updated_at: datetime


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
    created_at: datetime
    updated_at: datetime


class CategoryInfo(BaseModel):
    identifier: Optional[UUID]
    name: str
    is_enabled: bool


class TaxonomyInfo(BaseModel):
    identifier: Optional[UUID]
    keyword: str
    term: str
    description: Optional[str]
    tags: Optional[list[str]]
    is_enabled: bool


class EntityCrudInfo(BaseModel):
    name: str
    controller_model: Type[BaseModel]
    table_name: TableName
    field_map: Optional[dict[str, str]]


crud_entities = [
    EntityCrudInfo(
        name="entities",
        controller_model=EntityInfo,
        table_name=TableName.CONFIG_ENTITY
    ),
    EntityCrudInfo(
        name="observers",
        controller_model=ObserverInfo,
        table_name=TableName.CONFIG_OBSERVER,
        field_map={
            'config_entity.name': 'entity_name'
        }
    ),
    EntityCrudInfo(
        name="categories",
        controller_model=CategoryInfo,
        table_name=TableName.CONFIG_CATEGORY
    ),
    EntityCrudInfo(
        name="taxonomies",
        controller_model=TaxonomyInfo,
        table_name=TableName.CONFIG_TAXONOMY
    )
]
