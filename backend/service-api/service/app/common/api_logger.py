import json
import logging
import time
from typing import Optional
from uuid import UUID

from fastapi import Response, Request, HTTPException
from starlette.background import BackgroundTask
from starlette.responses import StreamingResponse
from starlette.types import Message

from service.app.auth.auth_models import AuthInfo
from service.app.auth.domain.client_auth_service import get_api_key
from service.app.auth.domain.session_service import get_session_id_from_header
from service.app.auth.domain.user_service import get_user_by_session
from service.common.infra.db.repository.core.api_log_audit_repository import ApiLogAuditEntity, insert_api_log_audit

logger = logging.getLogger(__name__)

# Add POST selectively for mutable API calls
mutable_methods = {"PUT", "DELETE", "PATCH"}
mutable_urls: list[str] = []


async def set_body(request: Request, body: bytes):
    async def receive() -> Message:
        return {'type': 'http.request', 'body': body}

    request._receive = receive


def is_mutable_api_call(request: Request, response: Response) -> bool:
    if request.method in mutable_methods:
        return True

    for url in mutable_urls:
        if request.url.path.startswith(url):
            return True

    if response.status_code >= 300:
        return True

    return False


def get_body(body: bytes) -> Optional[dict]:
    if not body:
        return None
    try:
        body_string = body.decode()
        try:
            return json.loads(body_string)
        except Exception as e:
            logger.exception(e)
            return {'wrong_body': body_string}
    except Exception as e:
        logger.exception(e)
    return None


async def log_requests(request: Request, call_next) -> Response:
    # Reference: https://stackoverflow.com/questions/69670125/how-to-log-raw-http-request-response-in-python-fastapi

    # Clone request body
    request_body = await request.body()
    await set_body(request, request_body)

    start_time = time.time_ns()
    response: Response | StreamingResponse = await call_next(request)

    # Don't log non-mutable and successful API calls
    if not is_mutable_api_call(request, response):
        return response

    try:
        process_time = (time.time_ns() - start_time) / 1000000

        tenant_id: Optional[UUID] = None
        user_id: Optional[UUID] = None
        api_auth_id: Optional[UUID] = None

        session_id = get_session_id_from_header(request.headers, request.cookies)
        if session_id:
            user_info = get_user_by_session(session_id)
            if user_info:
                user_id = UUID(user_info.identifier)
                tenant_id = user_info.preferred_tenant_id
        else:
            api_key = request.headers.get("x-api-key")
            tenant_code = request.headers.get("tenant-code")
            if api_key and tenant_code:
                try:
                    auth_info: AuthInfo = get_api_key(api_key, tenant_code)
                    if auth_info:
                        api_auth_id = auth_info.identifier
                        tenant_id = auth_info.tenant_id
                except HTTPException:
                    pass

        # Clone response body if possible
        response_body = b''
        async for chunk in response.body_iterator:  # type: ignore
            response_body += chunk  # type: ignore

        # Log the API call
        api_log_audit = ApiLogAuditEntity(
            request_url=request.url.path,
            request_method=request.method,
            request_headers=dict(request.headers),
            request_body=get_body(request_body),
            response_headers=dict(response.headers),
            response_body=get_body(response_body),
            status_code=response.status_code,
            processing_time=process_time,
            tenant_id=tenant_id,
            user_id=user_id,
            api_auth_id=api_auth_id
        )
        task = BackgroundTask(insert_api_log_audit, api_log_audit)
        response = Response(
            content=response_body,
            status_code=response.status_code,
            headers=dict(response.headers),
            media_type=response.media_type,
            background=task
        )

    except Exception as e:
        logger.exception(e)

    return response
