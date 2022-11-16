import logging

from fastapi import APIRouter, Depends
from fastapi import Cookie
from starlette import status
from starlette.exceptions import HTTPException
from starlette.responses import Response

from service.common.deps import (get_auth_handler, get_current_user)
from .model.request import LoginRequest
from ..domain.model.cache_models import UserSession
from ...common import http_utils

logger = logging.getLogger(__name__)

routes = APIRouter()


@routes.get("/session")
def get_current_session(user_info=Depends(get_current_user)):
    return user_info


@routes.post("/login")
def login_access_token(
        login_request: LoginRequest,
        response: Response,
        handler=Depends(get_auth_handler)):
    user_session: UserSession = handler.do_login(login_request.token)

    if not user_session:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect credential")
    else:
        logger.info("User logged-in: {}", user_session)

    if not user_session.preferred_org:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User without org")

    http_utils.set_cookie(response, "session_id", user_session.session_id, user_session.expiry_at)
    response.status_code = status.HTTP_204_NO_CONTENT


@routes.post("/logout")
def logout(response: Response, session_id: str = Cookie(default=None), handler=Depends(get_auth_handler)):
    http_utils.remove_cookie(response, "session_id")
    if session_id:
        user_info = handler.do_logout(session_id)
        if user_info:
            logger.info("User logged-out: {}", user_info)
            response.status_code = status.HTTP_204_NO_CONTENT
            return
    else:
        logger.error("Logout: session id is null")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Empty session")
