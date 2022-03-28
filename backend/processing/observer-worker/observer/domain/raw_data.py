from typing import Any, Dict, Optional

from pydantic import BaseModel


class RawData(BaseModel):
    identifier: Optional[int]
    company_id: int
    observer_id: int
    reference_id: str
    parent_reference_id: Optional[str]
    processing_status: Optional[str]
    tags: Optional[Dict[str, str]]
    raw_text: str
    data: Optional[Dict[str, Any]]
