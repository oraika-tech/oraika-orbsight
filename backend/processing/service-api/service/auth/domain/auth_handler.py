from typing import Optional

from pydantic import BaseSettings
from service.common.model.user import UserInfo

from .base import BasePersistenceManager


class AuthHandler(BaseSettings):
    persistence_manager: BasePersistenceManager

    def verify_user(self, email: str, password: str) -> Optional[UserInfo]:
        return self.persistence_manager.verify_user(email, password)

    def get_user_info(self, identifier: str) -> Optional[UserInfo]:
        return self.persistence_manager.get_user(identifier)
