from typing import Any, Optional

from pydantic import BaseModel

from service.app.auth.auth_db_provider import get_tenant_by_id_dp
from service.common.config.app_settings import app_settings
from service.common.infra.redis_provider import EntityRedisProvider


class TenantCache(BaseModel):
    org_id: Optional[str]
    tenant_id: str
    tenant_code: str
    tenant_name: str

    def __init__(self, entries=None, **data: Any):
        if entries:
            data.update(entries)
        super().__init__(**data)


_entity_manager = EntityRedisProvider('tnt')


def set_tenant(tenant: TenantCache, ttl: int = app_settings.DEFAULT_MAX_CACHE_TTL_SECONDS):
    _entity_manager.set_entity(tenant.tenant_id, vars(tenant), ttl=ttl)
    if tenant.org_id:
        _entity_manager.set_value(tenant.org_id, tenant.tenant_id, ttl=ttl)


def get_tenant_cache_by_id(tenant_id) -> Optional[TenantCache]:
    tenant_map = _entity_manager.get_entity(tenant_id)
    if tenant_map:
        return TenantCache(entries=tenant_map)
    else:  # tenant entry when not in cache
        tenant_info = get_tenant_by_id_dp(tenant_id)
        if tenant_info:
            return _save_and_get_cache(TenantCache(
                tenant_id=str(tenant_info.identifier),
                tenant_code=tenant_info.code,
                tenant_name=tenant_info.name
            ))
        else:
            return None


def _save_and_get_cache(tenant_cache: Optional[TenantCache]):
    if not tenant_cache:
        return None
    set_tenant(tenant_cache)
    return tenant_cache
