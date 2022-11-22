from typing import List, Optional

from pydantic import BaseModel

from service.auth.domain.model.domain_models import TenantInfo


class UserInfo(BaseModel):
    identifier: Optional[str]
    preferred_tenant_id: Optional[str]
    tenants: List[TenantInfo]
    name: Optional[str]
    email: Optional[str]
