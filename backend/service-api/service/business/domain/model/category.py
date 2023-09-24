from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class CategoryInfo(BaseModel):
    identifier: Optional[UUID]
    name: str
    is_enabled: bool
