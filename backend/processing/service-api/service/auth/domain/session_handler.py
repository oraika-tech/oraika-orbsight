import uuid
from typing import Any, Optional

from pydantic import BaseSettings, PrivateAttr

from service.auth.domain.model.cache_models import UserCache, TenantCache, UserSession, SessionCache, NileUser
from service.auth.persistence.redis_manager import EntityRedisManager
from service.common.settings import settings
from .base import BasePersistenceManager
from .model.domain_models import TenantInfo
from ...common.utils import now_epoch


class UserCacheManager(BaseSettings):
    _entity_manager: EntityRedisManager = PrivateAttr()

    def __init__(self, **values: Any):
        super().__init__(**values)
        self._entity_manager = EntityRedisManager('usr')

    def set_user(self, user_id: str, user: UserCache, ttl: int = settings.DEFAULT_MAX_CACHE_TTL_SECONDS):
        self._entity_manager.set_entity(user_id, user.to_dict(), ttl=ttl)

    def get_user(self, user_id: str) -> UserCache:
        user_cache = self._entity_manager.get_entity(user_id)
        return UserCache(entries=user_cache) if user_cache else None

    def update_user(self, user_id: str, field: str, value: any):
        self._entity_manager.update_entity(user_id, field, value)


class OrgCacheManager(BaseSettings):
    _entity_manager: EntityRedisManager = PrivateAttr()
    persistence_manager: BasePersistenceManager

    def __init__(self, **values: Any):
        super().__init__(**values)
        self._entity_manager = EntityRedisManager('org')

    def set_org(self, org_id: str, org: TenantCache, ttl: int = settings.DEFAULT_MAX_CACHE_TTL_SECONDS):
        self._entity_manager.set_entity(org_id, vars(org), ttl=ttl)

    def get_or_create_org(self, org_id) -> Optional[TenantCache]:
        tenant_map = self._entity_manager.get_entity(org_id)
        if tenant_map:
            return TenantCache(entries=tenant_map)
        else:  # tenant entry when not in cache
            tenant_info: TenantInfo = self.persistence_manager.get_tenant_by_nile_org_id(org_id)
            if not tenant_info:
                return None
            tenant_cache = TenantCache(
                org_id=org_id,
                tenant_id=str(tenant_info.identifier),
                tenant_code=tenant_info.code,
                tenant_name=tenant_info.name
            )
            self.set_org(org_id, tenant_cache)
            return tenant_cache


class SessionHandler(BaseSettings):
    _entity_manager: EntityRedisManager = PrivateAttr()
    user_cache_manager: UserCacheManager
    org_cache_manager: OrgCacheManager

    def __init__(self, **values: Any):
        super().__init__(**values)
        self._entity_manager = EntityRedisManager('ssn')

    def create_session(self, user_id: str, token: str, nile_user: NileUser, expiry_at: Optional[int]) -> UserSession:
        session_id = str(uuid.uuid4())
        user_cache = self.user_cache_manager.get_user(user_id)
        org_ids = nile_user.org_ids
        if not user_cache:
            # by default take first org as preferred org
            preferred_org_id = org_ids[0] if len(org_ids) > 0 else None
            user_cache = UserCache(
                user_id=user_id,
                user_name=nile_user.name,
                email=nile_user.email,
                preferred_org_id=preferred_org_id,
                org_ids=org_ids
            )
            self.user_cache_manager.set_user(user_id, user_cache)
        else:  # update existing attributes
            if nile_user.org_ids != user_cache.org_ids:  # update cache org if changed at Nile
                user_cache.org_ids = nile_user.org_ids
                self.user_cache_manager.update_user(user_id, "org_ids", ','.join(nile_user.org_ids))
            if nile_user.name != user_cache.user_name:
                user_cache.user_name = nile_user.name
                self.user_cache_manager.update_user(user_id, "user_name", nile_user.name)
            if nile_user.email != user_cache.email:
                user_cache.email = nile_user.email
                self.user_cache_manager.update_user(user_id, "email", nile_user.email)

        session_cache = SessionCache(
            session_id=session_id,
            user_id=user_id,
            nile_token=token
        )
        self._entity_manager.set_entity(session_id, vars(session_cache), expiry_at)

        return self.get_user_session_from_cache(session_cache, user_cache, expiry_at)

    def get_user_session_from_cache(self, session_cache: SessionCache, user_cache: UserCache, expiry_at: Optional[int]):
        tenants = []
        preferred_org = None
        for org_id in user_cache.org_ids:
            tenant = self.org_cache_manager.get_or_create_org(org_id)
            if tenant is not None:
                tenants.append(tenant)
                if tenant.org_id == user_cache.preferred_org_id:
                    preferred_org = tenant

        return UserSession(
            session_id=session_cache.session_id,
            user_id=session_cache.user_id,
            user_name=user_cache.user_name,
            email=user_cache.email,
            nile_token=session_cache.nile_token,
            preferred_org=preferred_org,
            tenants=tenants,
            expiry_at=expiry_at
        )

    def get_session(self, session_id) -> Optional[UserSession]:
        session_cache = self._entity_manager.get_entity(session_id)
        if not session_cache:
            return None
        basic_session = SessionCache(entries=session_cache)
        user = self.user_cache_manager.get_user(basic_session.user_id)
        expiry_at = None
        if 'ttl' in session_cache:
            expiry_at = now_epoch() + session_cache['ttl']
        return self.get_user_session_from_cache(basic_session, user, expiry_at)

    def delete_session(self, session_id) -> UserSession:
        user_session = self.get_session(session_id)
        self._entity_manager.delete_entity(session_id)
        return user_session
