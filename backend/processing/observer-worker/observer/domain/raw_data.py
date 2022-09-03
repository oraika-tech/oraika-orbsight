from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import UUID

from observer.presentation.model.observer_job_event import ObserverType
from pydantic import BaseModel


class RawData(BaseModel):
    identifier: Optional[int]
    observer_id: UUID
    reference_id: str
    parent_reference_id: Optional[str]
    raw_text: str
    unstructured_data: Optional[Dict[str, Any]]
    event_time: datetime
