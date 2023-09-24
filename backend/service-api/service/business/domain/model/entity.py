from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel


class EntityInfo(BaseModel):
    identifier: Optional[UUID]
    name: str
    tags: Optional[List[str]]
    is_enabled: bool
