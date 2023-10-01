from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel

from service.app.auth.auth_models import UserInfo, TenantInfo
from service.common.infra.db.repository.core.tenant_repository import get_tenant_by_ids, get_all_demo_tenants, get_tenant_by_id
from service.common.infra.db.repository.core.user_repository import get_user_by_id, get_user_by_email, UserEntity
from service.common.utils.reflection_utils import convert_model, convert_models


class UserInfoWrapper(BaseModel):
    hash_password: str
    user_info: UserInfo


def get_tenant_by_id_dp(tenant_id: UUID) -> Optional[TenantInfo]:
    tenant_entity = get_tenant_by_id(tenant_id)
    return convert_model(tenant_entity, TenantInfo)


def get_user_info_by_entity(user_entity: Optional[UserEntity]) -> Optional[UserInfo]:
    if user_entity:
        tenants = get_tenant_by_ids(user_entity.tenant_ids)
        return UserInfo(
            identifier=str(user_entity.identifier),
            tenants=tenants,
            name=user_entity.name,
            email=user_entity.email
        )
    return None


def get_user_info_by_id(user_id: str) -> Optional[UserInfo]:
    user_entity = get_user_by_id(user_id)
    return get_user_info_by_entity(user_entity)


def get_user_info_by_email(email: str) -> Optional[UserInfoWrapper]:
    user_entity = get_user_by_email(email)
    if not user_entity:
        return None

    user_info = get_user_info_by_entity(user_entity)
    if not user_info:
        return None

    return UserInfoWrapper(hash_password=user_entity.hash_password, user_info=user_info)


def get_all_demo_tenants_dp() -> List[TenantInfo]:
    tenant_entities = get_all_demo_tenants()
    return convert_models(tenant_entities, TenantInfo)
