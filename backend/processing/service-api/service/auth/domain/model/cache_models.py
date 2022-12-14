from typing import Any, List, Optional, Dict

from pydantic import BaseModel


class NileUser(BaseModel):
    email: str
    name: Optional[str]
    org_ids: List[str]


class UserCache(BaseModel):
    user_id: Optional[str]
    user_name: Optional[str]
    email: Optional[str]
    preferred_tenant_id: Optional[str]
    tenant_ids: List[str]

    def __init__(self, entries=None, **data: Any):
        if entries:
            if 'tenant_ids' in entries:
                entries['tenant_ids'] = entries['tenant_ids'].split(',')
            data.update(entries)
        super().__init__(**data)

    def to_dict(self) -> Dict[str, str]:
        obj_dict = {key: value for key, value in vars(self).items()}
        obj_dict['tenant_ids'] = ','.join(self.tenant_ids)
        return obj_dict


class TenantCache(BaseModel):
    org_id: Optional[str]
    tenant_id: str
    tenant_code: str
    tenant_name: str

    def __init__(self, entries=None, **data: Any):
        if entries:
            data.update(entries)
        super().__init__(**data)


class SessionBase(BaseModel):
    session_id: Optional[str]


class SessionCache(SessionBase):
    user_id: str
    nile_token: Optional[str]

    def __init__(self, entries=None, **data: Any):
        if entries:
            data.update(entries)
        super().__init__(**data)


class UserSession(SessionCache):
    email: Optional[str]
    user_name: Optional[str]
    preferred_tenant_id: Optional[str]
    tenants: List[TenantCache]
    expiry_at: Optional[int]
