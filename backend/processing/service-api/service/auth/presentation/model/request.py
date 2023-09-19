from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    username: EmailStr
    password: str


class DemoLoginRequest(BaseModel):
    email: EmailStr


class PreferredTenantRequest(BaseModel):
    preferred_tenant_id: str
