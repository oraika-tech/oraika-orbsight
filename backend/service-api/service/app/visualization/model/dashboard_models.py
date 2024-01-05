from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel

from service.common.models import ComponentLayoutDO


class Field(BaseModel):
    field: str


class DashboardDO(BaseModel):
    identifier: UUID
    frontend_keys: List[str]
    title: str
    component_layout: Optional[ComponentLayoutDO] = None
