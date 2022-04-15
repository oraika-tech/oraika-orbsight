from typing import Set, Dict, Union

from pydantic import BaseModel, Field


class TaxonomyData(BaseModel):
    categories: Set[str] = Field([])
    taxonomy_map: Dict[str, Set[str]] = Field({})
