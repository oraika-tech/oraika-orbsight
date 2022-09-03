from uuid import UUID

from pydantic import BaseModel

from analyzer.model.structure_data_request import StructuredData


class DBStoreRequest(BaseModel):
    structured_data: StructuredData
    raw_data_identifier: int
    tenant_id: UUID
