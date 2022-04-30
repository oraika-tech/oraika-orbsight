from service.auth.persistence.db_manager import UserDBManager
from service.auth.domain.auth_handler import AuthHandler

user_db_manager = UserDBManager()
auth_handler = AuthHandler(persistence_manager=user_db_manager)
