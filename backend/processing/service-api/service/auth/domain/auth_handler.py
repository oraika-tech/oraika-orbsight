from typing import Optional
from pydantic import BaseSettings

from .base import BasePersistenceManager
from service.common.model.user import UserInfo


class AuthHandler(BaseSettings):
    persistence_manager: BasePersistenceManager

    def verify_user(self, login_name: str, password: str) -> Optional[int]:
        return self.persistence_manager.verify_user(login_name, password)

    def user_info(self, identifier: int) -> Optional[UserInfo]:
        return self.persistence_manager.get_user(identifier)
