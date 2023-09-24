from abc import abstractmethod
from typing import Optional

from pydantic import BaseSettings

from service.common.model.user import UserInfo


class BasePersistenceManager(BaseSettings):

    @abstractmethod
    def verify_user(self, email: str, password: str) -> Optional[UserInfo]:
        pass

    @abstractmethod
    def get_user(self, identifier: str) -> Optional[UserInfo]:
        pass
