import logging

from fastapi import APIRouter, Depends
from starlette import status
from starlette.exceptions import HTTPException
from starlette.responses import Response

from service.common.deps import (get_auth_handler)
from .model.request import DemoLoginRequest
from ..domain.model.cache_models import UserSession
from ...common import http_utils

logger = logging.getLogger(__name__)

routes = APIRouter()


@routes.post("/demo-login")
def demo_login_email(
        login_request: DemoLoginRequest,
        response: Response,
        handler=Depends(get_auth_handler)):
    user_session: UserSession = handler.demo_login(login_request.email)

    if not user_session:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect credential")
    else:
        logger.info("User logged-in: {}", user_session)

    if not user_session.preferred_tenant_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User without org")

    http_utils.set_cookie(response, "orb_demo_session_id", user_session.session_id, user_session.expiry_at)
    response.status_code = status.HTTP_204_NO_CONTENT
