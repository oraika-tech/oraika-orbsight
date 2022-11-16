import logging

from starlette.responses import Response

from service.common.settings import settings
from service.common.utils import now_epoch

logger = logging.getLogger(__name__)


def set_cookie(response: Response, name, value, expiry_at):
    if expiry_at and expiry_at > 0:
        response.set_cookie(
            key=name,
            value=value,
            samesite='strict',
            secure=settings.COOKIE_SECURE,
            httponly=True,
            expires=(expiry_at - now_epoch())
        )
    else:
        logger.error("set_cookie without expiry")
        response.set_cookie(
            key=name,
            value=value,
            samesite='strict',
            secure=settings.COOKIE_SECURE,
            httponly=True,
            max_age=settings.DEFAULT_MAX_CACHE_TTL_SECONDS
        )


def remove_cookie(response: Response, name):
    response.delete_cookie(
        key=name,
        samesite='strict',
        secure=settings.COOKIE_SECURE,
        httponly=True
    )
