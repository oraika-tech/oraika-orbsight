from typing import Optional

from pydantic import BaseModel


class StatsInfo(BaseModel):
    name: str
    value: Optional[int]
