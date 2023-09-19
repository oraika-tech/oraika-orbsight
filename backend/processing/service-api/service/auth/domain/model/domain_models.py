from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class TenantInfo(BaseModel):
    identifier: Optional[UUID]
    name: str
    code: str
