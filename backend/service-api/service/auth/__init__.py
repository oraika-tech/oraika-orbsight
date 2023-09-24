from service.auth.domain.auth_handler import AuthHandler
from service.auth.domain.session_handler import SessionHandler, UserCacheManager, TenantCacheManager
from service.auth.persistence.redis_manager import EntityRedisManager
from service.common.db.tenant_entity_manager import TenantEntityManager
from service.common.db.user_entity_manager import UserEntityManager

user_db_manager = UserEntityManager()
tenant_entity_manager = TenantEntityManager()
user_cache_manager = UserCacheManager()
org_cache_manager = TenantCacheManager(tenant_entity_manager=tenant_entity_manager)

session_handler = SessionHandler(
    user_cache_manager=user_cache_manager,
    org_cache_manager=org_cache_manager
)

auth_handler = AuthHandler(
    persistence_manager=user_db_manager,
    tenant_entity_manager=tenant_entity_manager,
    user_cache_manager=user_cache_manager,
    org_cache_manager=org_cache_manager,
    session_handler=session_handler,
)
