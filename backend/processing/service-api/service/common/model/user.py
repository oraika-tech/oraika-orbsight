from typing import List, Optional

from pydantic import BaseModel


class UserInfo(BaseModel):
    identifier: Optional[str]
    tenant_ids: List[str]
    tenant_codes: List[str]
    name: Optional[str]
    email: Optional[str]
