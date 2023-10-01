from typing import Optional

from fastapi import Depends
from starlette import status
from starlette.exceptions import HTTPException
from starlette.responses import Response

from service.app.auth.auth_models import UserInfo, TenantInfo
from service.app.auth.domain.cache.session_cache_service import get_session
from service.app.auth.domain.cookie_utils import remove_cookie
from service.app.auth.domain.session_service import get_session_id, get_cookie_session_key


def get_current_user(response: Response,
                     session_id: str = Depends(get_session_id),
                     session_key=Depends(get_cookie_session_key)) -> UserInfo:
    user_info: Optional[UserInfo] = get_user_by_session(session_id)
    if not user_info or not user_info.preferred_tenant_id:
        remove_cookie(response, session_key)
        headers = {str(header[0]): str(header[1]) for header in response.raw_headers}
        status_code = status.HTTP_401_UNAUTHORIZED if not user_info else status.HTTP_403_FORBIDDEN
        raise HTTPException(status_code=status_code, detail="Unauthorized access", headers=headers)
    else:
        return user_info


def get_user_by_session(session_id: str) -> Optional[UserInfo]:
    if not session_id:
        return None

    user_session = get_session(session_id)
    if not user_session:
        return None

    tenants = [
        TenantInfo(
            identifier=tenant_cache.tenant_id,
            name=tenant_cache.tenant_name,
            code=tenant_cache.tenant_code,
        )
        for tenant_cache in user_session.tenants
    ]

    return UserInfo(
        identifier=user_session.user_id,
        tenants=tenants,
        preferred_tenant_id=user_session.preferred_tenant_id,
        name=user_session.user_name,
        email=user_session.email
    )
