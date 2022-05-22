from datetime import date, datetime
from typing import Optional, Union

from pydantic import BaseModel, validator


class FilterQueryParams(BaseModel):
    company_id: int
    start_date: Union[datetime, date] = None
    end_date: Union[datetime, date] = None
    entity_name: Optional[str] = None
    lang_code: Optional[str] = None
    observer_type: Optional[str] = None
    emotion: Optional[str] = None
    limit: Optional[int] = None
    # any field modification need changes at DataDomainHandler::hash_key() also

    @validator('entity_name', 'lang_code', 'observer_type', 'emotion')
    def set_all_as_none(cls, value):
        return None if value == 'All' else value
