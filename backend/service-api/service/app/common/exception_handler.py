import logging
from typing import Optional, Any
from uuid import UUID

from fastapi import HTTPException, status
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel
from starlette.requests import Request
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)


class ErrorData(BaseModel):
    message: str
    data: Optional[dict] = None


def http_exception_handler(request, exc):  # noqa
    if isinstance(exc.detail, ErrorData):
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": {"message": exc.detail.message, "data": exc.detail.data}},
        )
    else:
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": {"message": exc.detail}},
        )


def join_fields(fields: tuple) -> str:
    return '.'.join([str(field) for field in fields])


def validation_exception_handler(request: Request, exc: RequestValidationError):  # noqa
    try:
        if len(exc.errors()) > 0:
            error_data = {}
            error = exc.errors()[0]
            if error['type'] != 'json_invalid' and 'loc' in error:
                error_data['data'] = {'field': join_fields(error['loc'][1:])}
            if 'msg' in error:
                error_data['message'] = error['msg']
            if 'ctx' in error and 'error' in error['ctx']:
                error_data['message'] += ': ' + error['ctx']['error']
            return JSONResponse(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                content={"error": error_data}
            )
        else:
            logger.error(f"Validation error: {exc}")
            return JSONResponse(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                content={"error": {"message": "Validation error"}}
            )
    except Exception as e:
        logger.error(f"Validation error: {exc}")
        raise e


def clean_value(value: Any) -> Any:
    if isinstance(value, UUID):
        return str(value)
    else:
        return value


def http_exception(status_code: int, msg: str, data: Optional[dict] = None) -> HTTPException:
    if data:
        clean_data = {k: clean_value(v) for k, v in data.items() if v is not None}
        return HTTPException(
            status_code=status_code,
            detail=ErrorData(message=msg, data=clean_data)
        )
    else:
        return HTTPException(
            status_code=status_code,
            detail=msg
        )


def http_exception_unauthorized(msg: str, data: Optional[dict] = None) -> HTTPException:
    return http_exception(status.HTTP_401_UNAUTHORIZED, msg, data)
