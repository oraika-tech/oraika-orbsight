import logging

from starlette.responses import Response

from service.common.config.app_settings import app_settings
from service.common.utils.utils import now_epoch

logger = logging.getLogger(__name__)


def set_cookie(response: Response, name, value, expiry_at):
    if expiry_at and expiry_at > 0:
        response.set_cookie(
            key=name,
            value=value,
            samesite='strict',
            secure=app_settings.COOKIE_SECURE,
            httponly=True,
            expires=(expiry_at - now_epoch())
        )
    else:
        logger.error("set_cookie without expiry")
        response.set_cookie(
            key=name,
            value=value,
            samesite='strict',
            secure=app_settings.COOKIE_SECURE,
            httponly=True,
            max_age=app_settings.DEFAULT_MAX_CACHE_TTL_SECONDS
        )


def remove_cookie(response: Response, name):
    response.delete_cookie(
        key=name,
        samesite='strict',
        secure=app_settings.COOKIE_SECURE,
        httponly=True
    )
