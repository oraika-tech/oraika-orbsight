import logging
from enum import Enum
from http import HTTPStatus
from typing import List, Optional, TypeVar, Generic, Any, Type
from uuid import UUID

from fastapi import APIRouter, Depends, Body, Request
from pydantic import BaseModel
from starlette import status

from service.app.auth.domain.user_service import get_current_user
from service.app.common.exception_handler import http_exception
from service.app.generic.rest.rest_db_provider import RestTableProvider
from service.app.generic.rest.rest_models import EntityCrudInfo
from service.common.utils.utils import convert_to_pascal

logger = logging.getLogger(__name__)

M = TypeVar('M', bound=BaseModel)


class CrudController(Generic[M]):
    # Router
    routes: APIRouter
    prefix: str
    tags: list[str | Enum]
    # Controller
    table_provider: RestTableProvider[M]
    domain_model: Type[M]

    def __init__(self, domain_model: Type[M], entity_crud_info: EntityCrudInfo):
        # Router info
        self.routes = APIRouter()
        self.prefix = "/" + entity_crud_info.name
        self.tags = [convert_to_pascal(entity_crud_info.name)]
        # Controller info
        self.domain_model = domain_model
        self.table_provider = RestTableProvider[M](
            table_name=entity_crud_info.table_name,
            domain_model=self.domain_model,
            field_map=entity_crud_info.field_map
        )

        # Register routes
        self.register_routes()

    def register_routes(self):

        @self.routes.get("/{identifier}", response_model=self.domain_model)
        def get(identifier: UUID, user_info=Depends(get_current_user)) -> M:
            value: Optional[M] = self.table_provider.get(user_info.preferred_tenant_id, identifier)
            if not value:
                raise http_exception(status_code=404, msg="Not Found", data={"identifier": identifier})
            return value

        @self.routes.get("", response_model=List[self.domain_model])
        def search(request: Request,
                   _start: Optional[int] = None, _end: Optional[int] = None,
                   page_no: Optional[int] = None, page_size: Optional[int] = None,
                   user_info=Depends(get_current_user)) -> List[M]:

            options = dict(request.query_params)
            offset = None
            limit = None

            if _start is not None and _end is not None:
                if _end < 1:
                    raise http_exception(status_code=400, msg="Invalid _end")
                if _end <= _start:
                    raise http_exception(status_code=400, msg="Invalid _start and _end, _end should be greater than _start")
                del options['_start']
                del options['_end']
                offset = _start
                limit = _end - _start

            elif page_no is not None and page_size is not None:
                if page_no < 1:
                    raise http_exception(status_code=400, msg="Invalid page_no")
                if page_size < 1:
                    raise http_exception(status_code=400, msg="Invalid page_size")
                del options['page_no']
                del options['page_size']
                offset = (page_no - 1) * page_size
                limit = page_size

            elif _start is not None or _end or page_no is not None or page_size is not None:
                if _start is None or not _end:
                    missing_params = ['_start' if not _start else '_end']
                elif page_no is None or page_size is None:
                    missing_params = ['page_no' if not page_no else 'page_size']
                else:
                    missing_params = ['page_no', 'page_size']
                raise http_exception(status_code=400,
                                     msg="Missing pagination params",
                                     data={"missing_params": missing_params})

            return self.table_provider.search(tenant_id=user_info.preferred_tenant_id,
                                              options=options,
                                              offset=offset,
                                              limit=limit)

        @self.routes.post("", response_model=self.domain_model)
        def create(model: dict[str, Any] = Body(...), user_info=Depends(get_current_user)) -> M:
            value: Optional[M] = self.table_provider.create(user_info.preferred_tenant_id, model)
            if not value:
                raise http_exception(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, msg="Entity not created")
            return value

        @self.routes.patch("/{identifier}", response_model=self.domain_model)
        def update(identifier: UUID, update_fields: dict[str, Any], user_info=Depends(get_current_user)) -> M:
            if not update_fields:
                raise http_exception(status_code=400, msg="Empty patch request")
            update_value = self.table_provider.update(user_info.preferred_tenant_id, identifier, update_fields)
            if not update_value:
                raise http_exception(status_code=status.HTTP_404_NOT_FOUND, msg="Not Found", data={"identifier": identifier})
            return update_value

        @self.routes.delete("/{identifier}", response_model=self.domain_model)
        def delete(identifier: UUID, user_info=Depends(get_current_user)) -> M:
            value = self.table_provider.delete(user_info.preferred_tenant_id, identifier)
            if not value:
                raise http_exception(status_code=status.HTTP_404_NOT_FOUND, msg="Not Found", data={"identifier": identifier})
            return value
