import logging
from typing import Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel, EmailStr
from starlette import status
from starlette.exceptions import HTTPException
from starlette.responses import Response

from service.app.auth.auth_models import UserInfo
from service.app.auth.auth_service import set_preferred_tenant, do_login_with_credentials, do_logout, demo_login
from service.app.auth.domain.cache.session_cache_service import UserSession
from service.app.auth.domain.cookie_utils import set_cookie, remove_cookie
from service.app.auth.domain.session_service import get_cookie_session_key, get_session_id
from service.app.auth.domain.user_service import get_current_user
from service.app.common.exception_handler import http_exception

logger = logging.getLogger(__name__)

routes = APIRouter()


class PreferredTenantRequest(BaseModel):
    preferred_tenant_id: str


class LoginRequest(BaseModel):
    username: EmailStr
    password: str


class DemoLoginRequest(BaseModel):
    email: EmailStr


@routes.get("/session")
def get_current_session(user_info=Depends(get_current_user)):
    return user_info


@routes.post("/preferred-tenant")
def set_user_preferred_tenant(
        request: PreferredTenantRequest,
        response: Response,
        session_id: str = Depends(get_session_id),
        session_key=Depends(get_cookie_session_key)):
    user_info: Optional[UserInfo] = None
    try:
        user_info = get_current_user(response, session_id, session_key)
    except HTTPException as e:  # ignoring for setting preference first
        if e.status_code != status.HTTP_403_FORBIDDEN:
            raise e
    if not user_info:
        raise http_exception(status_code=status.HTTP_403_FORBIDDEN, msg="User not found")

    preferred_tenants = [tenant
                         for tenant in user_info.tenants
                         if str(tenant.identifier) == request.preferred_tenant_id]
    if len(preferred_tenants) != 1:
        raise http_exception(status_code=status.HTTP_403_FORBIDDEN, msg="Wrong tenant for user")

    set_preferred_tenant(user_info.identifier, request.preferred_tenant_id)
    response.status_code = status.HTTP_204_NO_CONTENT


@routes.post("/login")
def login_access_token(login_request: LoginRequest, response: Response) -> dict:
    user_session: Optional[UserSession] = do_login_with_credentials(login_request.username, login_request.password)

    if not user_session:
        raise http_exception(status_code=status.HTTP_400_BAD_REQUEST, msg="Incorrect credential")
    else:
        logger.info("User logged-in: {}", user_session)

    if not user_session.preferred_tenant_id:
        raise http_exception(status_code=status.HTTP_403_FORBIDDEN, msg="User without org")

    set_cookie(response, "web_session_id", user_session.session_id, user_session.expiry_at)
    response.status_code = status.HTTP_200_OK
    return {"status": "success"}


@routes.post("/logout")
def logout(response: Response, session_id: str = Depends(get_session_id), session_key=Depends(get_cookie_session_key)):
    if session_key:
        remove_cookie(response, session_key)
    if session_id:
        user_info = do_logout(session_id)
        if user_info:
            logger.info("User logged-out: {}", user_info)
            response.status_code = status.HTTP_204_NO_CONTENT
            return
    else:
        logger.error("Logout: session id is null")
        raise http_exception(status_code=status.HTTP_400_BAD_REQUEST, msg="Empty session")


@routes.post("/demo-login")
def demo_login_email(login_request: DemoLoginRequest, response: Response):
    user_session: Optional[UserSession] = demo_login(login_request.email)

    if not user_session:
        raise http_exception(status_code=status.HTTP_400_BAD_REQUEST, msg="Incorrect credential")
    else:
        logger.info("User logged-in: {}", user_session)

    if not user_session.preferred_tenant_id:
        raise http_exception(status_code=status.HTTP_403_FORBIDDEN, msg="User without org")

    set_cookie(response, "orb_demo_session_id", user_session.session_id, user_session.expiry_at)
    response.status_code = status.HTTP_204_NO_CONTENT
