from pydantic import BaseModel


class StatusRequest(BaseModel):
    enabled: bool
