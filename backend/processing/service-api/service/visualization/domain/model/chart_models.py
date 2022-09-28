from enum import Enum
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel


class DataSourceType(Enum):
    CUBE_JS = 'CUBE_JS'


class DataSourceSeriesDO(BaseModel):
    name: Optional[str]
    query: str


class FilterDO(BaseModel):
    name: str
    values: List[str]
    operator: Optional[str]

    def __hash__(self):
        return hash((self.name, tuple(self.values), self.operator,))


class FieldMappingDO(BaseModel):
    series: Optional[str]
    data_field: str
    chart_field: str


class ChartDBO(BaseModel):
    identifier: UUID
    chart_type: str
    chart_config: dict
    data_source_type: DataSourceType
    data_source_series: List[DataSourceSeriesDO]
    data_field_mapping: List[FieldMappingDO]


class ChartDO(BaseModel):
    identifier: UUID
    chart_config: dict
    series_data: List[dict]
