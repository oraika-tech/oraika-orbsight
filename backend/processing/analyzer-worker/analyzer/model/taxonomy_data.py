from typing import Set

from pydantic import BaseModel, Field


class TaxonomyData(BaseModel):
    tags: Set[str] = Field([])
    terms: Set[str] = Field([])
