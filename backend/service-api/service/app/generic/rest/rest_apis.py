from fastapi import APIRouter

from service.app.generic.rest.crud_controller import CrudController
from service.app.generic.rest.rest_models import crud_entities

routes = APIRouter()

for entity_crud_info in crud_entities:
    entity_crud_controller = CrudController[entity_crud_info.controller_model](  # type: ignore
        entity_crud_info.controller_model,
        entity_crud_info
    )
    routes.include_router(
        router=entity_crud_controller.routes,
        prefix=entity_crud_controller.prefix,
        tags=entity_crud_controller.tags)
