import logging
from datetime import datetime
from enum import Enum
from typing import Type, Any, Generic, Sequence
from typing import TypeVar, List, Union, Dict, Optional
from uuid import UUID

from pydantic import BaseModel
from sqlalchemy import MetaData, false
from sqlalchemy.engine import Engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import declarative_base
from sqlmodel import SQLModel, Session, select

from service.common.infra.db.db_utils import get_tenant_engine
from service.common.infra.db.repository.generic.crud_models import get_entity_models
from service.common.models import TableName

logger = logging.getLogger(__name__)
current_time = datetime.now()

ET = TypeVar('ET', bound=SQLModel)


class SortOrder(str, Enum):
    ASC = 'asc'
    DESC = 'desc'


class FieldOrdering(BaseModel):
    field: str
    order: SortOrder = SortOrder.ASC


class CrudTableManager(Generic[ET]):
    tenant_engine: Engine
    entity_model: Type[ET]

    def __init__(self, tenant_engine: Engine, entity_model: Type[ET]):
        self.tenant_engine = tenant_engine
        self.entity_model = entity_model

    def _where(self, query, field: str, value: Any):
        if hasattr(self.entity_model, field) and value is not None:
            if isinstance(value, UUID):
                value = str(value)
            query = query.where(getattr(self.entity_model, field) == value)
        return query

    def _sort(self, query, fields_ordering: list[FieldOrdering]):
        for field_ordering in fields_ordering:
            if hasattr(self.entity_model, field_ordering.field):
                column_field = getattr(self.entity_model, field_ordering.field)
                query = query.order_by(column_field.asc() if field_ordering.order == SortOrder.ASC else column_field.desc())
        return query

    @staticmethod
    def _complete_result(result: ET) -> ET:
        result.dict()  # Load lazy relationships before session is closed
        return result

    def _complete_results(self, results: Sequence[ET]) -> List[ET]:
        return [self._complete_result(result) for result in results if result]

    def get(self, identifier: Union[int, str, UUID]) -> Optional[ET]:
        with Session(self.tenant_engine) as session:
            query = select(self.entity_model)
            query = self._where(query, 'identifier', identifier)
            query = self._where(query, 'is_deleted', false())
            data = session.exec(query).first()
            if data:
                return self._complete_result(data)
            else:
                return None

    def search(self, options: Optional[dict[str, Any]] = None, offset: Optional[int] = None, limit: Optional[int] = None) -> List[ET]:
        with Session(self.tenant_engine) as session:
            query = select(self.entity_model)

            query = self._where(query, 'is_deleted', false())

            if options:
                for key, value in options.items():
                    query = self._where(query, key, value)

            query = self._sort(query, [
                FieldOrdering(field='is_enabled', order=SortOrder.DESC),
                FieldOrdering(field='updated_at', order=SortOrder.DESC)
            ])

            if offset:
                query = query.offset(offset)

            if limit:
                query = query.limit(limit)

            return self._complete_results(session.exec(query).all())

    def create(self, entity_obj: Dict[str, Any]) -> ET:
        with Session(self.tenant_engine) as session:
            obj = self.entity_model(**entity_obj)
            session.add(obj)
            session.commit()
            session.refresh(obj)
            return self._complete_result(obj)

    def update(self, identifier: Union[int, UUID], entity_obj: Dict[str, Any]) -> Optional[ET]:
        with Session(self.tenant_engine) as session:
            query = select(self.entity_model)
            query = self._where(query, 'identifier', identifier)
            query = self._where(query, 'is_deleted', false())
            data = session.exec(query).first()
            if data:
                for k, v in entity_obj.items():
                    setattr(data, k, v)
                session.add(data)
                session.commit()
                session.refresh(data)
                return self._complete_result(data)
            else:
                return None

    def delete(self, identifier: Union[int, UUID]) -> Optional[ET]:
        with Session(self.tenant_engine) as session:
            query = select(self.entity_model)
            query = self._where(query, 'identifier', identifier)
            query = self._where(query, 'is_deleted', false())
            data = session.exec(query).first()
            if data:
                if hasattr(data, 'is_deleted'):
                    data.is_deleted = True
                    session.add(data)
                else:
                    session.delete(data)
                session.commit()
                session.refresh(data)
                return self._complete_result(data)
            else:
                return None


class _DbManager:
    tenant_engine: Engine
    tables: dict[TableName, CrudTableManager]

    def __init__(self, tenant_id: UUID):
        self.tenant_engine = get_tenant_engine(tenant_id)
        self.tables = self._get_tables()

    class CustomBase:
        def dict(self):
            mapper = self.__mapper__  # noqa
            data = {c.key: getattr(self, c.key) for c in mapper.column_attrs}

            for name, relation in mapper.relationships.items():
                if not name.endswith('_collection'):
                    related_instance = getattr(self, name)
                    if related_instance is not None:
                        if relation.uselist:
                            # For relationships that return a list, convert each item to a dict
                            data[name] = [item.dict() for item in related_instance]
                        else:
                            # For relationships that return a single item, convert it to a dict
                            data[name] = related_instance.dict()

            return data

    def _get_tables(self):
        # Define Base
        metadata = MetaData()
        exposed_tables = [table_name.value for table_name in TableName]
        metadata.reflect(self.tenant_engine, only=exposed_tables)
        Base = automap_base(metadata=metadata, cls=declarative_base(cls=self.CustomBase))

        custom_entity_models = get_entity_models(Base)
        Base.prepare()

        return {
            table_name: CrudTableManager(
                tenant_engine=self.tenant_engine,
                entity_model=(custom_entity_models.get(table_name) or Base.classes[table_name.value])
            )
            for table_name in TableName
        }

    def get_table_manager(self, table_name: TableName) -> CrudTableManager:
        return self.tables[table_name]


_tenant_db_managers: dict[UUID, _DbManager] = {}


# Function to auto-select the correct table manager based on the tenant_id and table_name
def db_ops(tenant_id: UUID, table_name: TableName) -> CrudTableManager:
    if tenant_id not in _tenant_db_managers:
        _tenant_db_managers[tenant_id] = _DbManager(tenant_id)
    return _tenant_db_managers[tenant_id].get_table_manager(table_name)
