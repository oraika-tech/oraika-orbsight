from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel

from .raw_data import RawDataInfo


class ProcessedDataInfo(BaseModel):
    identifier: Optional[int]
    raw_data_id: int
    event_time: Optional[datetime]
    emotion: Optional[str]
    fraud: Optional[bool]
    complaint: Optional[bool]
    harassment: Optional[bool]
    access: Optional[bool]
    delay: Optional[bool]
    interface: Optional[bool]
    charges: Optional[bool]
    text_lang: Optional[str]
    entity_name: str
    regulated_entity_type: Optional[List[str]]
    observer_name: str
    observer_type: str
    raw_data: Optional[RawDataInfo]
