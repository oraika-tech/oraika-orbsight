from typing import Optional, Dict
from uuid import UUID

from pydantic import BaseModel


class AnalyzerJobRequest(BaseModel):
    tenant_id: UUID
    raw_data_id: int
    raw_text: str
    message: Optional[Dict]
