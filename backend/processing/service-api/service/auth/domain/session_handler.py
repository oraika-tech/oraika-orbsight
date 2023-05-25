import uuid
from typing import Any, Optional, List

from pydantic import BaseSettings, PrivateAttr

from service.auth.domain.model.cache_models import UserCache, TenantCache, UserSession, SessionCache, NileUser
from service.auth.persistence.redis_manager import EntityRedisManager
from service.common.settings import settings
from .base import BasePersistenceManager
from .model.domain_models import TenantInfo
from ...common.model.user import UserInfo
from ...common.utils import now_epoch


class UserCacheManager(BaseSettings):
    _entity_manager: EntityRedisManager = PrivateAttr()

    def __init__(self, **values: Any):
        super().__init__(**values)
        self._entity_manager = EntityRedisManager('usr')

    def set_user(self, user_id: str, user: UserCache, ttl: int = settings.DEFAULT_MAX_CACHE_TTL_SECONDS):
        self._entity_manager.set_entity(user_id, user.to_dict(), ttl=ttl)

    def get_user(self, user_id: str) -> Optional[UserCache]:
        user_cache = self._entity_manager.get_entity(user_id)
        return UserCache(entries=user_cache) if user_cache else None

    def update_user(self, user_id: str, field: str, value: Any):
        self._entity_manager.update_entity(user_id, field, value)

    def set_preferred_tenant(self, user_id: str, preferred_tenant_id: str):
        self._entity_manager.update_entity(user_id, 'preferred_tenant_id', preferred_tenant_id)


class TenantCacheManager(BaseSettings):
    _entity_manager: EntityRedisManager = PrivateAttr()
    persistence_manager: BasePersistenceManager

    def __init__(self, **values: Any):
        super().__init__(**values)
        self._entity_manager = EntityRedisManager('tnt')

    def set_tenant(self, tenant: TenantCache, ttl: int = settings.DEFAULT_MAX_CACHE_TTL_SECONDS):
        self._entity_manager.set_entity(tenant.tenant_id, vars(tenant), ttl=ttl)
        if tenant.org_id:
            self._entity_manager.set_value(tenant.org_id, tenant.tenant_id, ttl=ttl)

    def get_tenant_by_org(self, org_id) -> Optional[TenantCache]:
        tenant_id = self._entity_manager.get_value(org_id)
        if tenant_id:
            return self.get_tenant_by_id(tenant_id)

        tenant = self.persistence_manager.get_tenant_by_nile_org_id(org_id)
        return self._save_and_get_cache(tenant)

    def get_tenant_by_id(self, tenant_id) -> Optional[TenantCache]:
        tenant_map = self._entity_manager.get_entity(tenant_id)
        if tenant_map:
            return TenantCache(entries=tenant_map)
        else:  # tenant entry when not in cache
            tenant_info_list: List[TenantInfo] = self.persistence_manager.get_tenant_by_ids([tenant_id])
            if len(tenant_info_list) > 0:
                return self._save_and_get_cache(tenant_info_list[0])
            else:
                return None

    def _save_and_get_cache(self, tenant_info: Optional[TenantInfo]):
        if not tenant_info:
            return None
        tenant_cache = TenantCache(
            org_id=tenant_info.nile_org_id,
            tenant_id=str(tenant_info.identifier),
            tenant_code=tenant_info.code,
            tenant_name=tenant_info.name
        )
        self.set_tenant(tenant_cache)
        return tenant_cache


class SessionHandler(BaseSettings):
    _entity_manager: EntityRedisManager = PrivateAttr()
    user_cache_manager: UserCacheManager
    org_cache_manager: TenantCacheManager

    def __init__(self, **values: Any):
        super().__init__(**values)
        self._entity_manager = EntityRedisManager('ssn')

    def create_session_for_user(self, user_info: UserInfo) -> Optional[UserSession]:
        tenant_ids = [str(tenant.identifier) for tenant in user_info.tenants if tenant]
        return self.create_session(tenant_ids, user_info.identifier, user_info.email, user_info.name)

    def create_user_session(self, user_id: str, token: str, nile_user: NileUser,
                            expiry_at: Optional[int]) -> Optional[UserSession]:

        tenants = [self.org_cache_manager.get_tenant_by_org(org_id) for org_id in nile_user.org_ids]
        tenant_ids = [tenant.tenant_id for tenant in tenants if tenant]

        return self.create_session(tenant_ids, user_id, nile_user.email, nile_user.name, token, expiry_at)

    def create_session(self, tenant_ids: List[str],
                       user_id: str, email: str, name: Optional[str] = None,
                       token: Optional[str] = None, expiry_at: Optional[int] = None):

        if len(tenant_ids) == 0:
            return None

        session_id = str(uuid.uuid4())
        user_cache = self.user_cache_manager.get_user(user_id)

        if not user_cache:
            user_cache = UserCache(
                user_id=user_id,
                user_name=name,
                email=email,
                # by default take first org as preferred org
                preferred_tenant_id=tenant_ids[0],
                tenant_ids=tenant_ids
            )
            self.user_cache_manager.set_user(user_id, user_cache)
        else:  # update existing attributes from nile to cache
            if tenant_ids != user_cache.tenant_ids:  # update cache org if changed at Nile
                user_cache.tenant_ids = tenant_ids
                self.user_cache_manager.update_user(user_id, "tenant_ids", ','.join(tenant_ids))
            if name != user_cache.user_name:
                user_cache.user_name = name
                self.user_cache_manager.update_user(user_id, "user_name", name)
            if email != user_cache.email:
                user_cache.email = email
                self.user_cache_manager.update_user(user_id, "email", email)

        session_cache = SessionCache(
            session_id=session_id,
            user_id=user_id,
            nile_token=token
        )
        self._entity_manager.set_entity(session_id, vars(session_cache), expiry_at)

        return self.get_user_session_from_cache(session_cache, user_cache, expiry_at)

    def get_user_session_from_cache(self, session_cache: SessionCache, user_cache: UserCache, expiry_at: Optional[int]):
        tenants = []
        preferred_tenant_id = None
        for tenant_id in user_cache.tenant_ids:
            tenant = self.org_cache_manager.get_tenant_by_id(tenant_id)
            if tenant:
                tenants.append(tenant)
                if tenant.tenant_id == user_cache.preferred_tenant_id:
                    preferred_tenant_id = tenant.tenant_id

        return UserSession(
            session_id=session_cache.session_id,
            user_id=session_cache.user_id,
            user_name=user_cache.user_name,
            email=user_cache.email,
            nile_token=session_cache.nile_token,
            preferred_tenant_id=preferred_tenant_id,
            tenants=tenants,
            expiry_at=expiry_at
        )

    def get_session(self, session_id) -> Optional[UserSession]:
        session_cache = self._entity_manager.get_entity(session_id)
        if not session_cache:
            return None
        basic_session = SessionCache(entries=session_cache)
        user = self.user_cache_manager.get_user(basic_session.user_id)
        if not user:
            return None
        expiry_at = None
        if 'ttl' in session_cache:
            expiry_at = now_epoch() + session_cache['ttl']
        return self.get_user_session_from_cache(basic_session, user, expiry_at)

    def delete_session(self, session_id) -> Optional[UserSession]:
        user_session = self.get_session(session_id)
        self._entity_manager.delete_entity(session_id)
        return user_session
