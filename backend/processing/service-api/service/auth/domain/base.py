from abc import abstractmethod
from typing import Optional

from service.common.model.user import UserInfo
from pydantic import BaseSettings


class BasePersistenceManager(BaseSettings):

    @abstractmethod
    def verify_user(self, login_name: str, password: str) -> Optional[int]:
        pass

    @abstractmethod
    def get_user(self, identifier: int) -> Optional[UserInfo]:
        pass
