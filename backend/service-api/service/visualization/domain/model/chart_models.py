from enum import Enum
from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel

from service.visualization.domain.model.common_models import DataSourceSeriesDO


class DataSourceType(Enum):
    CUBE_JS = 'CUBE_JS'


class FilterDO(BaseModel):
    name: str
    values: Optional[List[str]]
    operator: Optional[str]

    def __hash__(self):
        return hash((self.name, tuple(self.values), self.operator,))


class FieldMappingDO(BaseModel):
    series_name: Optional[str]
    data_field: str
    chart_field: str


class FieldPivotDO(BaseModel):
    series_name: Optional[str]
    columns: List[str]
    field_name: Optional[str]


class DataTransformerMetaDO(BaseModel):
    field_mapping: Optional[List[FieldMappingDO]]
    field_pivoting: Optional[List[FieldPivotDO]]


class DatasetResult(BaseModel):
    dimensions: List[str]
    results: List[list]

    def get_dataset(self) -> list:
        return [self.dimensions] + self.results


class ChartDBO(BaseModel):
    identifier: UUID
    chart_type: str
    chart_config: dict
    data_source_type: DataSourceType
    data_source_series: List[DataSourceSeriesDO]
    data_transformer_meta: Optional[DataTransformerMetaDO]


class ChartDO(BaseModel):
    identifier: UUID
    chart_config: dict
    series_data: List[dict]
