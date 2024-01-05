import logging
import os

import uvicorn
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.gzip import GZipMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware

from service.app import api_router
from service.app.common.api_logger import log_requests
from service.app.common.exception_handler import http_exception_handler, validation_exception_handler
from service.app.generic.graphql import graphql_apis
from service.common.config.app_settings import app_settings

LOGLEVEL = os.environ.get('LOGLEVEL', 'INFO').upper()
logging.basicConfig(
    format="%(asctime)s - %(levelname)5s - [%(thread)d:%(threadName)s] - %(filename)s - %(name)s:%(lineno)d - %(message)s",
    datefmt="%m/%d/%Y %I:%M:%S %p",
    level=LOGLEVEL
)
logger = logging.getLogger(__name__)
logger.setLevel(LOGLEVEL)
logging.getLogger("httpx").setLevel(logging.WARNING)  # stop prefect verbose logging

PORT = app_settings.SERVICE_PORT

app = FastAPI(
    title="API Layer",
    debug=False,
    description="API Layer",
    docs_url=None,
    redoc_url="/docs"
)

# add api interceptor here to call log_requests function to log request and response
app.middleware("http")(log_requests)

app.add_middleware(GZipMiddleware, minimum_size=1000)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=app_settings.ALLOWED_HOSTS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=app_settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)  # type: ignore

app.include_router(api_router, prefix=app_settings.API_V1_STR)

if app_settings.IS_GRAPHQL:
    app.include_router(graphql_apis.routes)


@app.on_event("startup")
def app_init():
    # logger.info(f"Open http://127.0.0.1:{PORT}/redoc")
    logger.info(f"Open http://127.0.0.1:{PORT}/docs")
    logger.info(f"Open http://127.0.0.1:{PORT}/openapi.json")
    if app_settings.IS_GRAPHQL:
        logger.info(f"Open http://127.0.0.1:{PORT}/graphql")


is_multi_process = False

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=PORT, reload=True)
