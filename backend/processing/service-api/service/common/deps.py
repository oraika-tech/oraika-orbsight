import logging
from datetime import datetime, timedelta
from typing import Any, Optional, Union

from fastapi import Header, Depends, Cookie
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import BaseModel
from starlette import status
from starlette.exceptions import HTTPException
from starlette.responses import Response

from service.auth import auth_handler, session_handler
from service.common.settings import settings
from . import http_utils
from .model.user import UserInfo

logger = logging.getLogger(__name__)


class TokenPayload(BaseModel):
    sub: Optional[str] = None


reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login"
)


def get_auth_handler():
    return auth_handler


def get_session_handler():
    return session_handler


def create_access_token(subject: Union[str, int, Any], expires_delta: Optional[timedelta] = None) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def get_cookie_session_key(origin: str = Header()):
    if origin == settings.ORB_URL:
        return "web_session_id"
    elif origin == settings.DEMO_URL:
        return "orb_demo_session_id"
    else:
        return None


def get_session_id(origin: str = Header(),
                   web_session_id: str = Cookie(default=None),
                   orb_demo_session_id: str = Cookie(default=None)):
    if not origin:
        status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        raise HTTPException(status_code=status_code, detail="Empty origin")

    if origin == settings.ORB_URL or origin == settings.HOME_URL or origin == settings.WWW_URL:
        session_id = web_session_id
    elif origin == settings.DEMO_URL:
        session_id = orb_demo_session_id
    else:
        status_code = status.HTTP_401_UNAUTHORIZED
        raise HTTPException(status_code=status_code, detail="Empty session")

    return session_id


def get_current_user(response: Response,
                     session_id: str = Depends(get_session_id),
                     session_key=Depends(get_cookie_session_key),
                     handler=Depends(get_auth_handler)) -> UserInfo:
    user_info: Optional[UserInfo] = handler.get_user_by_session(session_id)
    if not user_info or not user_info.preferred_tenant_id:
        http_utils.remove_cookie(response, session_key)
        headers = {str(header[0]): str(header[1]) for header in response.raw_headers}
        status_code = status.HTTP_401_UNAUTHORIZED if not user_info else status.HTTP_403_FORBIDDEN
        raise HTTPException(status_code=status_code, detail="Unauthorized access", headers=headers)
    else:
        return user_info
