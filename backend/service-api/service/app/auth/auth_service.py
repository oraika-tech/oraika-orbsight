import logging
from typing import Optional

import bcrypt

from service.app.auth import auth_db_provider as db_provider
from service.app.auth.auth_db_provider import get_all_demo_tenants_dp
from service.app.auth.auth_models import UserInfo
from service.app.auth.domain.cache.session_cache_service import UserSession
from service.app.auth.domain.cache.session_cache_service import create_session_for_user, create_session, delete_session
from service.app.auth.domain.cache.user_cache_service import set_user_preferred_tenant

logger = logging.getLogger(__name__)


def do_login_with_credentials(email: str, password: str) -> Optional[UserSession]:
    user_info = verify_user(email, password)
    if user_info:
        return create_session_for_user(user_info)
    else:
        return None


def demo_login(email: str) -> Optional[UserSession]:
    demo_tenants = get_all_demo_tenants_dp()
    if not demo_tenants:
        return None
    demo_tenant_ids: list[str] = [str(tenant.identifier) for tenant in demo_tenants if tenant.identifier]
    return create_session(tenant_ids=demo_tenant_ids, user_id=email, email=email)


def do_logout(session_id: str):
    return delete_session(session_id)


def verify_user(email: str, password: str) -> Optional[UserInfo]:
    user_info_wrapper = db_provider.get_user_info_by_email(email)
    if user_info_wrapper:
        if bcrypt.checkpw(password.encode(), user_info_wrapper.hash_password.encode()):
            return user_info_wrapper.user_info
    return None


def get_user_info(identifier: str) -> Optional[UserInfo]:
    return db_provider.get_user_info_by_id(identifier)


def set_preferred_tenant(user_id: str, preferred_tenant_id: str):
    set_user_preferred_tenant(user_id, preferred_tenant_id)
