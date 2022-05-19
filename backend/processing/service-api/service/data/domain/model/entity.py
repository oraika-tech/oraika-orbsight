from typing import Optional

from pydantic import BaseModel


class DataEntity(BaseModel):
    id: Optional[int]
    name: str
