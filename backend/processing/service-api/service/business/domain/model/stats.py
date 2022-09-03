from typing import Optional, Any

from pydantic import BaseModel


class StatsInfo(BaseModel):
    name: str
    value: Optional[int]
