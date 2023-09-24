from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel


class TextAnalysisData(BaseModel):
    raw_data_id: int
    event_time: Optional[datetime]
    emotion: Optional[str]
    entity_name: str
    observer_name: str
    observer_type: str
    raw_text: str
    text_lang: Optional[str]
    author_name: Optional[str]
    categories: List[str]
    taxonomy_tags: List[str]
    taxonomy_terms: List[str]
