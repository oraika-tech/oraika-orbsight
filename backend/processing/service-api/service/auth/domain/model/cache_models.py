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
    preferred_org_id: str
    org_ids: List[str]

    def __init__(self, entries=None, **data: Any):
        if entries:
            if 'org_ids' in entries:
                entries['org_ids'] = entries['org_ids'].split(',')
            data.update(entries)
        super().__init__(**data)

    def to_dict(self) -> Dict[str, str]:
        obj_dict = vars(self)
        obj_dict['org_ids'] = ','.join(self.org_ids)
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
    nile_token: str

    def __init__(self, entries=None, **data: Any):
        if entries:
            data.update(entries)
        super().__init__(**data)


class UserSession(SessionCache):
    email: Optional[str]
    user_name: Optional[str]
    preferred_org: Optional[TenantCache]
    tenants: List[TenantCache]
    expiry_at: Optional[int]
