from datetime import date, datetime
from typing import Optional, Union
from uuid import UUID

from pydantic import BaseModel, validator


class FilterQueryParams(BaseModel):
    tenant_id: UUID
    start_date: Union[datetime, date] = None
    end_date: Union[datetime, date] = None
    entity_name: Optional[str] = None
    observer_name: Optional[str] = None
    term: Optional[str] = None
    tags: Optional[str] = None
    lang_code: Optional[str] = None
    observer_type: Optional[str] = None
    emotion: Optional[str] = None
    limit: Optional[int] = None

    # any name modification need changes at DataDomainHandler::hash_key() also

    @validator('entity_name', 'lang_code', 'observer_type', 'emotion', 'term', 'tags', 'observer_name')
    def set_all_as_none(cls, value):
        return None if value == 'All' else value
