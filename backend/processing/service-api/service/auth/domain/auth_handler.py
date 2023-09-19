import logging
from typing import Optional

from pydantic import BaseSettings

from service.common.model.user import UserInfo
from .base import BasePersistenceManager
from .model.cache_models import UserSession
from .model.domain_models import TenantInfo
from .session_handler import UserCacheManager, TenantCacheManager, SessionHandler

logger = logging.getLogger(__name__)


class AuthHandler(BaseSettings):
    persistence_manager: BasePersistenceManager
    user_cache_manager: UserCacheManager
    org_cache_manager: TenantCacheManager
    session_handler: SessionHandler

    def do_login_with_credentials(self, email: str, password: str) -> Optional[UserSession]:
        user_info = self.persistence_manager.verify_user(email, password)
        if user_info:
            return self.session_handler.create_session_for_user(user_info)
        else:
            return None

    def demo_login(self, email: str) -> Optional[UserSession]:
        demo_tenants = self.persistence_manager.get_demo_tenants()
        if not demo_tenants:
            return None
        demo_tenant_ids = [str(tenant.identifier) for tenant in demo_tenants]
        return self.session_handler.create_session(tenant_ids=demo_tenant_ids, user_id=email, email=email)

    def do_logout(self, session_id: str):
        return self.session_handler.delete_session(session_id)

    def verify_user(self, email: str, password: str) -> Optional[UserInfo]:
        return self.persistence_manager.verify_user(email, password)

    def get_user_info(self, identifier: str) -> Optional[UserInfo]:
        return self.persistence_manager.get_user(identifier)

    def get_user_by_session(self, session_id: str) -> Optional[UserInfo]:
        if not session_id:
            return None

        user_session = self.session_handler.get_session(session_id)
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

    def set_preferred_tenant(self, user_id: str, preferred_tenant_id: str):
        self.user_cache_manager.set_preferred_tenant(user_id, preferred_tenant_id)
