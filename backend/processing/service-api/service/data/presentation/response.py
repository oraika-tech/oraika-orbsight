from pydantic import BaseModel


class DataResponse(BaseModel):
    text: str
    emotion: str
