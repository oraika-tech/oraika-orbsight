import dataclasses
import json
from typing import Optional, List
from uuid import UUID

import strawberry
from strawberry.scalars import ID, JSON

from service.app.generic.graphql.graphql_db_provider import get_all_entities, get_by_id, search
from service.app.generic.graphql.graphql_models import TaxonomyInfo, ObserverInfo, EntityInput, EntityInfo


def get_domain_value(entity_obj, domain_field: dataclasses.Field):
    if dataclasses.is_dataclass(domain_field.type):
        fields = {field.name: field for field in dataclasses.fields(domain_field.type)}
        domain_dict = {
            key: get_domain_value(value, fields[key])
            for key, value in entity_obj.items()
            if key in fields
        }
        # Ensure domain_field.type is callable before using it
        if callable(domain_field.type):
            return domain_field.type(**domain_dict)
        else:
            raise TypeError(f"The type {domain_field.type} is not callable.")
    else:
        return entity_obj


def entity_to_domain(entity_obj, domain_model: type):
    fields = {field.name: field for field in dataclasses.fields(domain_model)}  # noqa

    domain_dict = {
        column.name: get_domain_value(getattr(entity_obj, column.name), fields[column.name])
        for column in entity_obj.__table__.columns
        if column.name in fields
    }
    return domain_model(**domain_dict)


table_name_to_model_name = {
    'config_entity': EntityInfo,
    'config_observer': ObserverInfo,
    'config_taxonomy': TaxonomyInfo
}


def fetch_data(table_name: str | type, identifier: Optional[UUID], search_terms: Optional[str]):
    if search_terms:
        entities = search(table_name, json.loads(search_terms))
    elif identifier:
        entities = [get_by_id(table_name, str(identifier))]
    else:
        entities = get_all_entities(table_name)
    model_name = table_name_to_model_name[table_name if isinstance(table_name, str) else table_name.__name__]
    return [entity_to_domain(entity, model_name) for entity in entities]


# Generate GraphQL types dynamically
# types = {table_name: strawberry.type(table_obj) for table_name, table_obj in get_table_objects().items()}


@strawberry.type
class Query:

    @strawberry.field(name="entity")
    def entity(self, id: ID) -> EntityInfo:
        return fetch_data('config_entity', UUID(id), None)[0]

    @strawberry.field(name="entities")
    def entities(self, sort: Optional[str] = None, where: Optional[JSON] = None,  # type: ignore
                 start: Optional[int] = None, limit: Optional[int] = None) -> List[EntityInfo]:
        return fetch_data('config_entity', None, None)

    @strawberry.field(name="observers")
    def observers(self, identifier: Optional[UUID] = None, search_terms: Optional[str] = None) -> List[ObserverInfo]:
        return fetch_data('config_observer', identifier, search_terms)

    @strawberry.field(name="taxonomies")
    def taxonomies(self, identifier: Optional[UUID] = None, search_terms: Optional[str] = None) -> List[TaxonomyInfo]:
        return fetch_data('config_taxonomy', identifier, search_terms)


@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_entity(self, entity: EntityInput) -> EntityInfo:
        return EntityInfo(identifier=UUID('8283c1f2-2ea6-457b-883a-b37e7d7d98d4'), name=entity.name, tags=entity.tags, is_enabled=entity.is_enabled)

    @strawberry.mutation
    def update_entity(self, entity: EntityInput) -> EntityInfo:
        return EntityInfo(identifier=UUID('123'), name=entity.name, tags=entity.tags, is_enabled=entity.is_enabled)
