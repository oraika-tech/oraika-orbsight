import logging
from datetime import datetime
from uuid import UUID

from sqlalchemy import MetaData, false
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

from service.common.infra.db.db_utils import get_tenant_engine

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
    Entity = _get_entity(table)
    return session.query(Entity).all()


def get_all(table: str | type, page: int = 1, items_per_page: int = 10):
    Entity = _get_entity(table)
    return session.query(Entity) \
        .filter(Entity.is_deleted == false()) \
        .offset((page - 1) * items_per_page) \
        .limit(items_per_page) \
        .all()


def get_by_id(table: str | type, identifier: str | int):
    Entity = _get_entity(table)
    return session.query(Entity) \
        .filter(Entity.identifier == identifier, Entity.is_deleted == false()) \
        .first()


def search(table: str | type, kwargs: dict):
    Entity = _get_entity(table)
    query = session.query(Entity).filter(Entity.is_deleted == false())
    for key, value in kwargs.items():
        query = query.filter(getattr(Entity, key) == value)
    return query.all()


def create(table: str, entity_obj: dict):
    Entity = _get_entity(table)
    session.add(Entity(**entity_obj))
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
