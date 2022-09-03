from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel


class TaxonomyInfo(BaseModel):
    identifier: Optional[UUID]
    keyword: str
    term: str
    description: Optional[str]
    tags: Optional[List[str]]
    is_enabled: bool
