import uuid
from typing import Any, Optional, List

from pydantic import BaseModel

from service.app.auth.auth_models import UserInfo
from service.app.auth.domain.cache.tenant_cache_service import TenantCache, get_tenant_cache_by_id
from service.app.auth.domain.cache.user_cache_service import get_user, UserCache, set_user, update_user
from service.common.infra.redis_provider import EntityRedisProvider
from service.common.utils.utils import now_epoch


class SessionBase(BaseModel):
    session_id: Optional[str] = None


class SessionCache(SessionBase):
    user_id: str

    def __init__(self, entries=None, **data: Any):
        if entries:
            data.update(entries)
        super().__init__(**data)


class UserSession(SessionCache):
    email: Optional[str] = None
    user_name: Optional[str] = None
    preferred_tenant_id: Optional[str] = None
    tenants: List[TenantCache]
    expiry_at: Optional[int] = None


_entity_manager = EntityRedisProvider('ssn')


def create_session_for_user(user_info: UserInfo) -> Optional[UserSession]:
    tenant_ids = [str(tenant.identifier) for tenant in user_info.tenants if tenant and tenant.identifier]
    return create_session(tenant_ids, user_info.identifier, user_info.email, user_info.name)


def create_session(tenant_ids: List[str],
                   user_id: str, email: str, name: Optional[str] = None,
                   expiry_at: Optional[int] = None):
    if len(tenant_ids) == 0:
        return None

    session_id = str(uuid.uuid4())
    user_id_str = str(user_id)
    user_cache = get_user(user_id_str)

    if not user_cache:
        user_cache = UserCache(
            user_id=user_id_str,
            user_name=name,
            email=email,
            # by default take first org as preferred org
            preferred_tenant_id=tenant_ids[0],
            tenant_ids=tenant_ids
        )
        set_user(user_id_str, user_cache)
    else:  # update existing attributes from db to cache
        if tenant_ids != user_cache.tenant_ids:
            user_cache.tenant_ids = tenant_ids
            update_user(user_id_str, "tenant_ids", ','.join(user_cache.tenant_ids))
        if name != user_cache.user_name:
            user_cache.user_name = name
            update_user(user_id_str, "user_name", name)
        if email != user_cache.email:
            user_cache.email = email
            update_user(user_id_str, "email", email)

    session_cache = SessionCache(
        session_id=session_id,
        user_id=user_id_str,
    )
    _entity_manager.set_entity(session_id, vars(session_cache), expiry_at)

    return get_user_session_from_cache(session_cache, user_cache, expiry_at)


def get_user_session_from_cache(session_cache: SessionCache, user_cache: UserCache, expiry_at: Optional[int]):
    tenants = []
    preferred_tenant_id = None
    for tenant_id in user_cache.tenant_ids:
        tenant = get_tenant_cache_by_id(tenant_id)
        if tenant:
            tenants.append(tenant)
            if tenant.tenant_id == user_cache.preferred_tenant_id:
                preferred_tenant_id = tenant.tenant_id

    return UserSession(
        session_id=session_cache.session_id,
        user_id=session_cache.user_id,
        user_name=user_cache.user_name,
        email=user_cache.email,
        preferred_tenant_id=preferred_tenant_id,
        tenants=tenants,
        expiry_at=expiry_at
    )


def get_session(session_id) -> Optional[UserSession]:
    session_cache = _entity_manager.get_entity(session_id)
    if not session_cache:
        return None
    basic_session = SessionCache(entries=session_cache)
    user = get_user(basic_session.user_id)
    if not user:
        return None
    expiry_at = None
    if 'ttl' in session_cache:
        expiry_at = now_epoch() + session_cache['ttl']
    return get_user_session_from_cache(basic_session, user, expiry_at)


def delete_session(session_id) -> Optional[UserSession]:
    user_session = get_session(session_id)
    _entity_manager.delete_entity(session_id)
    return user_session
