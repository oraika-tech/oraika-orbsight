from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel


class UserInfo(BaseModel):
    identifier: Optional[UUID]
    tenant_ids: List[str]
    name: str
    email: str
