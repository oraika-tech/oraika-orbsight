from pydantic import BaseModel, EmailStr


class SessionRequest(BaseModel):
    nile_token: str


class LoginRequest(BaseModel):
    username: EmailStr
    password: str


class DemoLoginRequest(BaseModel):
    email: EmailStr


class PreferredTenantRequest(BaseModel):
    preferred_tenant_id: str
