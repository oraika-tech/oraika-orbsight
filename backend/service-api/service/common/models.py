from datetime import datetime, date
from enum import Enum
from typing import Union, Optional, List, Any
from uuid import UUID

from pydantic import BaseModel, validator


class TableName(Enum):
    CONFIG_CATEGORY = 'config_category'
    CONFIG_ENTITY = 'config_entity'
    CONFIG_OBSERVER = 'config_observer'
    CONFIG_TAXONOMY = 'config_taxonomy'
    INSIGHT_PROCESSED_DATA = 'insight_processed_data'
    INSIGHT_RAW_DATA = 'insight_raw_data'
    TENANT_CONFIG = 'tenant_config'
    VIZ_CHART = 'viz_chart'
    VIZ_DASHBOARD = 'viz_dashboard'
    WORKFLOW_NODE_META = 'workflow_node_meta'


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


# --------------- Base Models ---------------------------

class HeaderAlias(BaseModel):
    column: str
    header: str


class Pivoting(BaseModel):
    columns: List[str]
    field_name: str


class FieldValue(BaseModel):
    field: str
    value: Any


# --------------- Dependent Models ---------------------------

class DataSourceSeriesDO(BaseModel):
    name: Optional[str] = None
    query: str
    pivot_columns: Optional[List[str]] = None
    header_alias: Optional[List[HeaderAlias]] = None


class DataMapping(BaseModel):
    mappings: List[dict]
    pivoting: Pivoting


class Component(BaseModel):
    identifier: Optional[UUID] = None
    title: Optional[str] = None
    type: str
    xs: Optional[float] = None
    sm: Optional[float] = None
    md: Optional[float] = None
    lg: Optional[float] = None
    xl: Optional[float] = None
    height: Optional[str] = None
    name: Optional[str] = None
    class_name: Optional[str] = None
    categories: Optional[List[str]] = None
    dock_align: Optional[str] = None  # left, right, top, bottom
    components: Optional[List['Component']] = None

    inputs: Optional[List[FieldValue]] = []
    outputs: Optional[List[str]] = []
    disabled: Optional[bool] = None


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
