
from fastapi import APIRouter

from service.auth.presentation import auth_routes
from service.business.presentation import entity_routes
from service.business.presentation import observer_routes
from service.business.presentation import taxonomy_routes
from service.data.presentation import data_api_routes

api_router = APIRouter()
api_router.include_router(auth_routes.routes, prefix="/auth", tags=["auth"])
api_router.include_router(entity_routes.routes, prefix="/entities", tags=["business"])
api_router.include_router(observer_routes.routes, prefix="/observers", tags=["business"])
api_router.include_router(taxonomy_routes.routes, prefix="/taxonomies", tags=["business"])
api_router.include_router(data_api_routes.routes, prefix="/data", tags=["data"])
