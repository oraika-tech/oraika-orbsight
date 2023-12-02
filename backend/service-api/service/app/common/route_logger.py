import json
import logging
import time
from typing import Callable, Optional
from uuid import UUID

from fastapi import Request, Response
from fastapi.routing import APIRoute
from starlette.concurrency import run_in_threadpool

from service.app.auth.auth_models import AuthInfo
from service.app.auth.domain.client_auth_service import get_api_key
from service.app.auth.domain.session_service import get_session_id_from_header
from service.app.auth.domain.user_service import get_user_by_session
from service.common.infra.db.repository.core.api_log_audit_repository import ApiLogAuditEntity, insert_api_log_audit

logger = logging.getLogger(__name__)


class TimedRoute(APIRoute):
    mutable_methods = {"POST", "PUT", "DELETE", "PATCH"}

    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:

            # only log mutable methods
            if request.method not in self.mutable_methods:
                return await original_route_handler(request)

            # Clone request body
            request_body = await request.body()

            start_time = time.time_ns()
            # Call the original handler
            try:
                response: Response = await original_route_handler(request)
            except Exception as e:
                logger.exception(e)
                raise e

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
                        auth_info: AuthInfo = get_api_key(api_key, tenant_code)
                        if auth_info:
                            api_auth_id = auth_info.identifier
                            tenant_id = auth_info.tenant_id

                # Clone response body if possible
                response_body = b''
                if hasattr(response, 'body'):
                    response_body = response.body

                # Log the API call
                api_log_audit = ApiLogAuditEntity(
                    request_url=request.url.path,
                    request_method=request.method,
                    request_headers=dict(request.headers),
                    request_body=json.loads(request_body.decode()) if request_body else None,
                    response_headers=dict(response.headers),
                    response_body=json.loads(response_body.decode()) if response_body else None,
                    status_code=response.status_code,
                    processing_time=process_time,
                    tenant_id=tenant_id,
                    user_id=user_id,
                    api_auth_id=api_auth_id
                )
                await run_in_threadpool(insert_api_log_audit, api_log_audit)
            except Exception as e:
                logger.exception(e)

            return response

        return custom_route_handler
