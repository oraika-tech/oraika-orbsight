from typing import Generic, Union, Optional, Any, Type, TypeVar
from uuid import UUID

from pydantic import BaseModel

from service.common.infra.db.repository.generic.crud_repository import CrudTableManager, db_ops
from service.common.models import TableName
from service.common.utils.reflection_utils import convert_model, convert_models

DM = TypeVar('DM', bound=BaseModel)


class RestTableProvider(Generic[DM]):
    domain_model: Type[DM]
    field_map: Optional[dict[str, str]] = None
    table_name: TableName
    tenant_table_manager: dict[UUID, CrudTableManager]

    def __init__(self, table_name: TableName, domain_model: Type[DM], field_map: Optional[dict[str, str]] = None):
        self.domain_model = domain_model
        self.table_name = table_name
        self.tenant_table_manager = {}
        self.field_map = field_map

    def _get_table_manager(self, tenant_id: UUID) -> CrudTableManager:
        if tenant_id not in self.tenant_table_manager:
            self.tenant_table_manager[tenant_id] = db_ops(tenant_id, self.table_name)
        return self.tenant_table_manager[tenant_id]

    def _convert_model(self, entity_obj: Any) -> Optional[DM]:
        return convert_model(entity_obj, self.domain_model, self.field_map)

    def _convert_models(self, entity_obj: list) -> list[DM]:
        return convert_models(entity_obj, self.domain_model, self.field_map)

    def get(self, tenant_id: UUID, identifier: Union[int, UUID]) -> Optional[DM]:
        entity_obj = self._get_table_manager(tenant_id).get(identifier)
        return self._convert_model(entity_obj)

    def search(self, tenant_id: UUID, options: Optional[dict[str, Any]] = None,
               offset: Optional[int] = None, limit: Optional[int] = None) -> list[DM]:
        entity_obj = self._get_table_manager(tenant_id).search(options, offset, limit)
        return self._convert_models(entity_obj)

    def create(self, tenant_id: UUID, model_obj: dict[str, Any]) -> Optional[DM]:
        entity_obj = self._get_table_manager(tenant_id).create(model_obj)
        return self._convert_model(entity_obj)

    def update(self, tenant_id: UUID, identifier: Union[int, UUID], entity_obj: dict[str, Any]) -> Optional[DM]:
        updated_obj = self._get_table_manager(tenant_id).update(identifier, entity_obj)
        return self._convert_model(updated_obj)

    def delete(self, tenant_id: UUID, identifier: Union[int, UUID]) -> Optional[DM]:
        entity_obj = self._get_table_manager(tenant_id).delete(identifier)
        return self._convert_model(entity_obj)
