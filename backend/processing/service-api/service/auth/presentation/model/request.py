from pydantic import BaseModel


class SessionRequest(BaseModel):
    nile_token: str


class LoginRequest(BaseModel):
    token: str


class PreferredTenantRequest(BaseModel):
    preferred_tenant_id: str
