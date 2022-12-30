import logging
from typing import Optional

from jose import jwt
from pydantic import BaseSettings

from service.common.model.user import UserInfo
from .base import BasePersistenceManager
from .model.cache_models import UserSession
from .model.domain_models import TenantInfo
from .session_handler import UserCacheManager, TenantCacheManager, SessionHandler
from ..persistence.nile_client import NileClient
from ...common.settings import settings

logger = logging.getLogger(__name__)


class AuthHandler(BaseSettings):
    persistence_manager: BasePersistenceManager
    user_cache_manager: UserCacheManager
    org_cache_manager: TenantCacheManager
    session_handler: SessionHandler
    nile_client: NileClient

    '''
        JWT token data format
        {
            "jti": "usr_02rTROOozYSsKgJUydETt0",            // JWT ID
            "iss": "nile",                                  // issuer
            "user_type": "USER",                            // USER: normal user
            "parent_org_id": "org_02rI1exlhuwgqyWfxJvUGO",  // useless for now
            "iat": 1667971711,                              // issue at in epoch
            "sub": "girish.patel@oraika.com",               // user email
            "exp": 1668058111                               // expiry in epoch
        }
    '''

    def do_login(self, token: str) -> Optional[UserSession]:
        is_valid = self.nile_client.validate_user_token(token)
        if is_valid:
            payload = jwt.decode(token, '', options={'verify_signature': False}, algorithms=[settings.ALGORITHM])
            user_id = payload['jti']
            expiry_at = payload['exp']
            nile_user = self.nile_client.get_user_info(user_id)
            if nile_user:
                if len(nile_user.org_ids) == 0:
                    logger.error("User without any tenant")
                else:
                    return self.session_handler.create_user_session(user_id, token, nile_user, expiry_at)
        else:
            logger.error("User token invalid")

        return None

    def demo_login(self, email: str) -> Optional[UserSession]:
        demo_tenants = self.persistence_manager.get_demo_tenants()
        if demo_tenants is None:
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
        if user_session is None:
            return None

        tenants = [
            TenantInfo(
                identifier=tenant_cache.tenant_id,
                name=tenant_cache.tenant_name,
                code=tenant_cache.tenant_code,
                nile_org_id=tenant_cache.org_id
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
