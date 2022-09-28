from fastapi import APIRouter

from service.auth.presentation import auth_routes
from service.business.presentation import (dashboard_routes, entity_routes, category_routes,
                                           observer_routes, taxonomy_routes)
from service.data.presentation import data_api_routes, grafana_api_routes
from service.visualization.presentation import dashboard_api_routes

api_router = APIRouter()
api_router.include_router(auth_routes.routes, prefix="/auth", tags=["auth"])
api_router.include_router(dashboard_routes.routes, prefix="/dashboards", tags=["dashboard"])
api_router.include_router(dashboard_api_routes.routes, prefix="/visualization", tags=["visualization"])
api_router.include_router(entity_routes.routes, prefix="/entities", tags=["business"])
api_router.include_router(observer_routes.routes, prefix="/observers", tags=["business"])
api_router.include_router(taxonomy_routes.routes, prefix="/taxonomies", tags=["business"])
api_router.include_router(category_routes.routes, prefix="/categories", tags=["business"])
api_router.include_router(data_api_routes.routes, prefix="/data", tags=["data"])
api_router.include_router(grafana_api_routes.routes, prefix="/grafana", tags=["data"])
