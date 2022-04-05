from datetime import datetime
from typing import Any, Dict, Optional, List

from pydantic import BaseModel

from observer.presentation.model.observer_job_event import ObserverType


class RawData(BaseModel):
    identifier: Optional[int]
    company_id: int
    observer_id: int
    observer_name: str
    observer_type: ObserverType
    entity_id: int
    entity_name: str
    regulated_entity_type: List[str]
    reference_id: str
    parent_reference_id: Optional[str]
    processing_status: Optional[str]
    tags: Optional[Dict[str, str]]
    raw_text: str
    data: Optional[Dict[str, Any]]
    event_time: datetime
