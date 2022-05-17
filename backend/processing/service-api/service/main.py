import logging

import uvicorn
from fastapi import FastAPI, HTTPException
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.gzip import GZipMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from service import api_router
from service.common.settings import settings

logger = logging.getLogger(__name__)
PORT = 8080


async def http_error_handler(_: Request, exc: HTTPException) -> JSONResponse:
    return JSONResponse({"errors": [exc.detail]}, status_code=exc.status_code)


app = FastAPI(
    title="API Layer",
    debug=False,
    description="API Layer"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(GZipMiddleware, minimum_size=1000)

app.add_middleware(
    TrustedHostMiddleware, allowed_hosts=settings.ALLOWED_HOSTS
)

app.add_exception_handler(HTTPException, http_error_handler)

app.include_router(api_router, prefix=settings.API_V1_STR)


@app.on_event("startup")
def app_init():
    logger.info(f"Open http://127.0.0.1:{PORT}/redoc")
    logger.info(f"Open http://127.0.0.1:{PORT}/docs")
    logger.info(f"Open http://127.0.0.1:{PORT}/openapi.json")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=PORT)
