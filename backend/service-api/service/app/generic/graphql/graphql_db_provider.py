import logging
from datetime import datetime
from typing import Type, Callable, Any
from uuid import UUID

from pydantic import BaseModel
from sqlalchemy import MetaData, false
from sqlalchemy.ext.automap import automap_base
from sqlmodel import SQLModel, select, Session

from service.app.business.business_models import CategoryInfo, EntityInfo, ObserverInfo, OBSERVER_TYPE, TaxonomyInfo
from service.app.generic.graphql.graphql_models import ObserverData
from service.common.infra.db.db_utils import get_tenant_engine
from service.common.infra.db.repository.business.category_repository import CategoryEntity
from service.common.infra.db.repository.business.entity_repository import Entity
from service.common.infra.db.repository.business.observer_repository import ObserverEntity
from service.common.infra.db.repository.business.taxonomy_repository import TaxonomyEntity
from service.common.utils.utils import search_dict

logger = logging.getLogger(__name__)

exposed_tables = ['config_category', 'config_entity', 'config_observer', 'config_taxonomy', 'insight_processed_data',
                  'insight_raw_data', 'tenant_config', 'viz_chart', 'viz_dashboard', 'workflow_node_meta']

# todo: modify to accept tenant id from caller
tenant_id = UUID('02ddd60c-2d58-47cc-a445-275d8e621252')
engine = get_tenant_engine(tenant_id)
session = Session(engine)

metadata = MetaData()
metadata.reflect(engine, only=exposed_tables)
Base = automap_base(metadata=metadata)
Base.prepare()
current_time = datetime.now()


def convert_to_model_category(entity) -> CategoryInfo:
    return CategoryInfo(
        identifier=entity.identifier,
        name=entity.name,
        is_enabled=entity.is_enabled,
    )


def convert_to_model_entity(self) -> EntityInfo:
    return EntityInfo(
        identifier=self.identifier,
        name=self.name,
        tags=self.tags,
        is_enabled=self.is_enabled,
    )


def convert_to_model_observer(self) -> ObserverInfo:
    data_json = self.config_data
    official_handle = next(search_dict(data_json, 'official_handle'), None)
    url = next(search_dict(data_json, 'url'), None)
    observer_type_str = OBSERVER_TYPE.get(self.type)
    return ObserverInfo(
        identifier=self.identifier,
        name=self.name,
        entity_id=self.entity_id,
        entity_name=self.entity.name if self.entity else '',
        is_enabled=self.is_enabled,
        type=observer_type_str,
        config_data=ObserverData(
            official_handle=official_handle,
            url=url
        )
    )


def convert_to_model_config(self) -> TaxonomyInfo:
    return TaxonomyInfo(
        identifier=self.identifier,
        term=self.term,
        keyword=self.keyword,
        description=self.description,
        tags=self.tags,
        is_enabled=self.is_enabled
    )


entity_converter: dict[Type[SQLModel], Callable[[Any], BaseModel]] = {
    CategoryEntity: convert_to_model_category,
    Entity: convert_to_model_entity,
    ObserverEntity: convert_to_model_observer,
    TaxonomyEntity: convert_to_model_config
}


def get_table_objects() -> dict:
    return {
        table_name.capitalize(): type(
            table_name.capitalize(),
            (object,),
            {col.name: eval(col.type.python_type.__name__) for col in table_obj.__table__.columns}
        )
        for table_name, table_obj in Base.classes.items()
        if table_name in exposed_tables
    }


def _get_entity(table):
    return Base.classes[table] if isinstance(table, str) else table


def get_all_entities(table):
    TableModel = _get_entity(table)
    return session.exec(select(TableModel)).all()


def get_all(table: str | type, page: int = 1, items_per_page: int = 10):
    TableModel = _get_entity(table)
    return session.exec(
        select(TableModel)
        .where(TableModel.is_deleted == false())
        .offset((page - 1) * items_per_page)
        .limit(items_per_page)
    ).all()


def get_by_id(table: str | type, identifier: str | int):
    TableModel = _get_entity(table)
    return session.exec(
        select(TableModel)
        .where(TableModel.identifier == identifier, TableModel.is_deleted == false())
    ).first()


def search(table: str | type, kwargs: dict):
    TableModel = _get_entity(table)
    query = select(TableModel).where(TableModel.is_deleted == false())
    for key, value in kwargs.items():
        query = query.filter(getattr(TableModel, key) == value)
    return session.exec(query).all()


def create(table: str, entity_obj: dict):
    TableModel = _get_entity(table)
    session.add(TableModel(**entity_obj))
    session.commit()


def update(table: str, identifier, entity_obj: dict):
    data = get_by_id(table, identifier)
    for k, v in entity_obj.items():
        setattr(data, k, v)
    session.add(data)
    session.commit()


def delete(table: str, identifier):
    data = get_by_id(table, identifier)
    data.is_delete = True
    session.add(data)
    session.commit()
