from typing import List, Optional, Any
from uuid import UUID

from pydantic import BaseModel


class Field(BaseModel):
    field: str


class FieldValue(BaseModel):
    field: str
    value: Any


class Component(BaseModel):
    identifier: Optional[UUID]
    type: str
    width: float
    height: Optional[str]
    name: Optional[str]
    categories: Optional[List[str]]
    dock_align: Optional[str]  # left, right, top, bottom

    inputs: Optional[List[FieldValue]] = []
    outputs: Optional[List[str]] = []
    disabled: Optional[bool]


class ComponentLayoutDO(BaseModel):
    spacing: int
    components: List[Component]


class DashboardDO(BaseModel):
    identifier: UUID
    frontend_keys: List[str]
    title: str
    component_layout: Optional[ComponentLayoutDO]
