from typing import Set, Dict, Union

from pydantic import BaseModel, Field


class EntityData(BaseModel):
    categories: Set[str] = Field([])
    tags: Set[str] = Field([])
    entity_map: Dict[str, Set[str]] = Field({})
