import logging

from fastapi import APIRouter, Depends
from starlette import status
from starlette.exceptions import HTTPException
from starlette.responses import Response

from service.common.deps import (get_auth_handler, get_current_user, get_session_id, get_cookie_session_key)
from .model.request import LoginRequest, PreferredTenantRequest
from ..domain.model.cache_models import UserSession
from ...common import http_utils

logger = logging.getLogger(__name__)

routes = APIRouter()


@routes.get("/session")
def get_current_session(user_info=Depends(get_current_user)):
    return user_info


@routes.post("/preferred-tenant")
def set_user_preferred_tenant(
        request: PreferredTenantRequest,
        response: Response,
        session_id: str = Depends(get_session_id),
        session_key=Depends(get_cookie_session_key),
        handler=Depends(get_auth_handler)):
    try:
        user_info = get_current_user(response, session_id, session_key, handler)
    except HTTPException as e:  # ignoring for setting preference first
        if e.status_code != status.HTTP_403_FORBIDDEN:
            raise e

    preferred_tenants = [tenant for tenant in user_info.tenants if
                         str(tenant.identifier) == request.preferred_tenant_id]
    if len(preferred_tenants) != 1:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Wrong tenant for user")

    handler.set_preferred_tenant(user_info.identifier, request.preferred_tenant_id)
    response.status_code = status.HTTP_204_NO_CONTENT


@routes.post("/login")
def login_access_token(
        login_request: LoginRequest,
        response: Response,
        handler=Depends(get_auth_handler)) -> dict:
    user_session: UserSession = handler.do_login_with_credentials(login_request.username, login_request.password)

    if not user_session:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect credential")
    else:
        logger.info("User logged-in: {}", user_session)

    if not user_session.preferred_tenant_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User without org")

    http_utils.set_cookie(response, "web_session_id", user_session.session_id, user_session.expiry_at)
    response.status_code = status.HTTP_200_OK
    return {"status": "success"}


@routes.post("/logout")
def logout(response: Response,
           session_id: str = Depends(get_session_id),
           session_key=Depends(get_cookie_session_key),
           handler=Depends(get_auth_handler)):
    if session_key:
        http_utils.remove_cookie(response, session_key)
    if session_id:
        user_info = handler.do_logout(session_id)
        if user_info:
            logger.info("User logged-out: {}", user_info)
            response.status_code = status.HTTP_204_NO_CONTENT
            return
    else:
        logger.error("Logout: session id is null")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Empty session")
