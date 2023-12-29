from typing import Optional, List
from uuid import UUID

import strawberry


@strawberry.input()
class EntityInput:
    name: str
    tags: Optional[List[str]]
    is_enabled: bool


@strawberry.type
class EntityInfo:
    identifier: UUID
    name: str
    tags: Optional[List[str]]
    is_enabled: bool

    @strawberry.field(name="id")
    def id(self) -> UUID:
        return self.identifier


@strawberry.type
class ObserverData:
    official_handle: Optional[str] = None
    url: Optional[str] = None


@strawberry.type
class ObserverInfo:
    identifier: Optional[UUID]
    name: str
    type: str
    entity_id: UUID
    config_data: ObserverData
    is_enabled: bool


@strawberry.type
class TaxonomyInfo:
    identifier: Optional[UUID]
    keyword: str
    term: str
    description: Optional[str]
    tags: Optional[List[str]]
    is_enabled: bool
