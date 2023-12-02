from typing import Optional

from fastapi import Header, Cookie
from starlette import status
from starlette.datastructures import Headers
from starlette.exceptions import HTTPException

from service.common.config.app_settings import app_settings


def is_prod_url(origin: str) -> bool:
    return origin == app_settings.ORB_URL or origin == app_settings.HOME_URL or origin == app_settings.WWW_URL


def get_cookie_session_key(origin: str = Header()):
    if is_prod_url(origin):
        return "web_session_id"
    elif origin == app_settings.DEMO_URL:
        return "orb_demo_session_id"
    else:
        return None


def get_session_id(origin: str = Header(),
                   web_session_id: str = Cookie(default=None),
                   orb_demo_session_id: str = Cookie(default=None)) -> str:
    if not origin:
        status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        raise HTTPException(status_code=status_code, detail="Empty origin")

    if is_prod_url(origin):
        session_id = web_session_id
    elif origin == app_settings.DEMO_URL:
        session_id = orb_demo_session_id
    else:
        status_code = status.HTTP_401_UNAUTHORIZED
        raise HTTPException(status_code=status_code, detail="Empty session")

    return session_id


def get_session_id_from_header(headers: Headers, cookies: dict) -> Optional[str]:
    """ To be used by api logger"""
    if headers:
        origin = headers.get("origin")
        if origin:
            if is_prod_url(origin):
                return cookies.get("orb-session-id")
    return None
