from abc import abstractmethod
from typing import Optional, List

from pydantic import BaseSettings

from service.auth.domain.model.domain_models import TenantInfo
from service.common.model.user import UserInfo


class BasePersistenceManager(BaseSettings):

    @abstractmethod
    def verify_user(self, email: str, password: str) -> Optional[UserInfo]:
        pass

    @abstractmethod
    def get_user(self, identifier: str) -> Optional[UserInfo]:
        pass

    @abstractmethod
    def get_tenant_by_ids(self, tenant_ids) -> List[TenantInfo]:
        pass

    @abstractmethod
    def get_tenant_by_nile_org_id(self, nile_org_id) -> Optional[TenantInfo]:
        pass
