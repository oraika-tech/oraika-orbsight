from uuid import UUID

from pydantic import BaseModel


class AnalyzerAPIRequest(BaseModel):
    tenant_id: UUID
    raw_data_id: int
    raw_text: str


class AnalyzerAPIResponse(BaseModel):
    identifier: int
