from pydantic import BaseModel


class DataSourceType(BaseModel):
    name: str
