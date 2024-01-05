from typing import Optional, List
from uuid import UUID

import strawberry


@strawberry.input()
class EntityInput:
    name: str
    tags: Optional[List[str]] = None
    is_enabled: bool


@strawberry.type
class EntityInfo:
    identifier: UUID
    name: str
    tags: Optional[List[str]] = None
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
    identifier: Optional[UUID] = None
    name: str
    type: str
    entity_id: UUID
    config_data: ObserverData
    is_enabled: bool


@strawberry.type
class TaxonomyInfo:
    identifier: Optional[UUID] = None
    keyword: str
    term: str
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    is_enabled: bool
