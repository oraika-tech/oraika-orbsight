from typing import Optional, Any

from pydantic import BaseModel


class StatsInfo(BaseModel):
    name: str
    value: Optional[int]

    def as_dict(self):
        return {
            "Name": self.name,
            "Count": self.value
        }
