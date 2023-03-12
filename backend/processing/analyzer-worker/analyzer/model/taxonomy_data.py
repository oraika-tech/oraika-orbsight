from typing import Set

from pydantic import BaseModel, Field


class TaxonomyData(BaseModel):
    tags: Set[str] = Field(set())
    terms: Set[str] = Field(set())
