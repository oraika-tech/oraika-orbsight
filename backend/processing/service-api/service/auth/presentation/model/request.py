from pydantic import BaseModel


class SessionRequest(BaseModel):
    nile_token: str


class LoginRequest(BaseModel):
    token: str
