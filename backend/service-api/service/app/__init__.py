from fastapi import APIRouter

from service.app.auth import auth_apis
from service.app.business.business_apis import category_apis, taxonomy_apis, observer_apis, entity_apis
from service.app.data import data_apis, data_public_apis
from service.app.visualization import visualization_apis

api_router = APIRouter()
api_router.include_router(auth_apis.routes, prefix="/auth", tags=["Auth"], include_in_schema=False)
api_router.include_router(visualization_apis.routes, prefix="/visualization", tags=["Visualization"], include_in_schema=False)
api_router.include_router(entity_apis.routes, prefix="/entities", tags=["Business"], include_in_schema=False)
api_router.include_router(observer_apis.routes, prefix="/observers", tags=["Business"], include_in_schema=False)
api_router.include_router(taxonomy_apis.routes, prefix="/taxonomies", tags=["Business"], include_in_schema=False)
api_router.include_router(category_apis.routes, prefix="/categories", tags=["Business"], include_in_schema=False)
api_router.include_router(data_apis.routes, prefix="/data", tags=["Data"], include_in_schema=False)
api_router.include_router(data_public_apis.routes, prefix="/public/data", tags=["Data"])
