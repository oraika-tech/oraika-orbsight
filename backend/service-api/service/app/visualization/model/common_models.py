from typing import List, Optional

from pydantic import BaseModel

from service.common.models import HeaderAlias


class OrderData(BaseModel):
    field: str
    is_reverse: bool


class SortOrder(BaseModel):
    order: List[OrderData]
    is_all_numbers: bool


class ConfigData(BaseModel):
    key_columns: List[HeaderAlias]

    header: str
    pivot: Optional[bool] = None
