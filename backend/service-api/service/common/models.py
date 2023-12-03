from datetime import datetime, date
from enum import Enum
from typing import Union, Optional, List, Any
from uuid import UUID

from pydantic import BaseModel, validator


class TenantType(int, Enum):
    TEST = -1
    DEMO = 0
    CORPORATE = 1
    GOV = 2
    INDIVIDUAL = 3


class DataSourceType(str, Enum):
    CUBE_JS = 'CUBE_JS'


class NodeMetaState(str, Enum):
    SENT = 'SENT'
    FAILED = 'FAILED'


# Base Models
class HeaderAlias(BaseModel):
    column: str
    header: str


class Pivoting(BaseModel):
    columns: List[str]
    field_name: str


class FieldValue(BaseModel):
    field: str
    value: Any


# Dependent Models
class DataSourceSeriesDO(BaseModel):
    name: Optional[str]
    query: str
    pivot_columns: Optional[List[str]]
    header_alias: Optional[List[HeaderAlias]]


class DataMapping(BaseModel):
    mappings: List[dict]
    pivoting: Pivoting


class Component(BaseModel):
    identifier: Optional[UUID]
    title: Optional[str]
    type: str
    xs: Optional[float]
    sm: Optional[float]
    md: Optional[float]
    lg: Optional[float]
    xl: Optional[float]
    height: Optional[str]
    name: Optional[str]
    class_name: Optional[str]
    categories: Optional[List[str]]
    dock_align: Optional[str]  # left, right, top, bottom
    components: Optional[List['Component']]

    inputs: Optional[List[FieldValue]] = []
    outputs: Optional[List[str]] = []
    disabled: Optional[bool]


class ComponentLayoutDO(BaseModel):
    spacing: int
    components: List[Component]


class FilterQueryParams(BaseModel):
    tenant_id: UUID
    start_date: Union[datetime, date, None] = None
    end_date: Union[datetime, date, None] = None
    entity_name: Optional[str] = None
    observer_name: Optional[str] = None
    term: Optional[str] = None
    tags: Optional[str] = None
    lang_code: Optional[str] = None
    observer_type: Optional[str] = None
    emotion: Optional[str] = None
    limit: Optional[int] = None
    raw_data_id: Optional[int] = None

    @validator('entity_name', 'lang_code', 'observer_type', 'emotion', 'term', 'tags', 'observer_name')
    def set_all_as_none(cls, value):  # noqa
        return None if value == 'All' else value
