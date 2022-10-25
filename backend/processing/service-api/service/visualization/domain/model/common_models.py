from typing import List

from pydantic import BaseModel


class OrderData(BaseModel):
    field: str
    is_reverse: bool


class SortOrder(BaseModel):
    order: List[OrderData]
    is_all_numbers: bool
