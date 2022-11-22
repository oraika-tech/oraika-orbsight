from service.auth.domain.auth_handler import AuthHandler
from service.auth.domain.session_handler import SessionHandler, UserCacheManager, TenantCacheManager
from service.auth.persistence.db_manager import UserDBManager
from service.auth.persistence.nile_client import NileClient
from service.auth.persistence.redis_manager import EntityRedisManager

user_db_manager = UserDBManager()
user_cache_manager = UserCacheManager()
org_cache_manager = TenantCacheManager(persistence_manager=user_db_manager)
nile_client = NileClient()

session_handler = SessionHandler(
    user_cache_manager=user_cache_manager,
    org_cache_manager=org_cache_manager
)

auth_handler = AuthHandler(
    persistence_manager=user_db_manager,
    user_cache_manager=user_cache_manager,
    org_cache_manager=org_cache_manager,
    session_handler=session_handler,
    nile_client=nile_client
)
