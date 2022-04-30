from datetime import datetime
from typing import Optional, List, Dict, Any

from pydantic import BaseModel


class RawDataInfo(BaseModel):
    identifier: Optional[int]
    observer_id: int
    observer_name: str
    observer_type: str
    entity_id: int
    entity_name: str
    regulated_entity_type: List[str]
    raw_text: str
    data: Optional[Dict[str, Any]]
    event_time: Optional[datetime]
