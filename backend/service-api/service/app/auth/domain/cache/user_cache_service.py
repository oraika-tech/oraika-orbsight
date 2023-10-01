from typing import Any, Optional, List, Dict

from pydantic import BaseModel

from service.common.config.app_settings import app_settings
from service.common.infra.redis_provider import EntityRedisProvider


class UserCache(BaseModel):
    user_id: Optional[str]
    user_name: Optional[str]
    email: Optional[str]
    preferred_tenant_id: Optional[str]
    tenant_ids: List[str]

    def __init__(self, entries=None, **data: Any):
        if entries:
            if 'tenant_ids' in entries:
                entries['tenant_ids'] = entries['tenant_ids'].split(',')
            data.update(entries)
        super().__init__(**data)

    def to_dict(self) -> Dict[str, str]:
        obj_dict = {key: value for key, value in vars(self).items()}
        obj_dict['tenant_ids'] = ','.join(self.tenant_ids)
        return obj_dict


_entity_manager = EntityRedisProvider('usr')


def set_user(user_id: str, user: UserCache, ttl: int = app_settings.DEFAULT_MAX_CACHE_TTL_SECONDS):
    _entity_manager.set_entity(user_id, user.to_dict(), ttl=ttl)


def get_user(user_id: str) -> Optional[UserCache]:
    user_cache = _entity_manager.get_entity(user_id)
    return UserCache(entries=user_cache) if user_cache else None


def update_user(user_id: str, field: str, value: Any):
    _entity_manager.update_entity(user_id, field, value)


def set_user_preferred_tenant(user_id: str, preferred_tenant_id: str):
    _entity_manager.update_entity(user_id, 'preferred_tenant_id', preferred_tenant_id)
