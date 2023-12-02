from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel


class TenantInfo(BaseModel):
    identifier: Optional[UUID]
    name: str
    code: str


class UserInfo(BaseModel):
    identifier: str
    preferred_tenant_id: Optional[UUID]
    tenants: List[TenantInfo]
    name: Optional[str]
    email: str


class ApiAuthInfo(BaseModel):
    identifier: UUID
    name: str
    hashed_key: str


class AuthInfo(BaseModel):
    identifier: UUID
    tenant_id: UUID
