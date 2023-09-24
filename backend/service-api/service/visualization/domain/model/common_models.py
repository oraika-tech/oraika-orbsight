from typing import List, Optional

from pydantic import BaseModel


class OrderData(BaseModel):
    field: str
    is_reverse: bool


class SortOrder(BaseModel):
    order: List[OrderData]
    is_all_numbers: bool


class HeaderAlias(BaseModel):
    column: str
    header: str


class ConfigData(BaseModel):
    key_columns: List[HeaderAlias]

    header: str
    pivot: Optional[bool]


class DataSourceSeriesDO(BaseModel):
    name: Optional[str]
    query: str
    pivot_columns: Optional[List[str]]
    header_alias: Optional[List[HeaderAlias]]


class DataConfig(BaseModel):
    key_columns: List[HeaderAlias]
    series: List[DataSourceSeriesDO]
