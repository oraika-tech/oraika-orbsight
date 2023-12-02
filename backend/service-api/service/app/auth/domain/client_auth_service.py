import bcrypt
from fastapi import Depends, Header
from fastapi.security import APIKeyHeader

from service.app.auth import auth_db_provider as db_provider
from service.app.auth.auth_models import AuthInfo
from service.app.common.exception_handler import http_exception_unauthorized

API_KEY_NAME = "x-api-key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)


def get_api_key(api_key: str = Depends(api_key_header), tenant_code: str = Header()) -> AuthInfo:
    if not api_key:
        raise http_exception_unauthorized(msg="Empty API Key", data={"api_key": api_key})

    if not tenant_code:
        raise http_exception_unauthorized(msg="Empty Tenant Code", data={"tenant_code": tenant_code})

    tenant_info = db_provider.get_tenant_by_code_dp(tenant_code)
    if not tenant_info or not tenant_info.identifier:
        # raise get_exception("Invalid Tenant Code")
        raise http_exception_unauthorized(msg="Invalid Tenant Code", data={"tenant_code": tenant_code})

    api_auth_info_list = db_provider.get_api_auth_by_tenant_id_dp(tenant_info.identifier)
    if not api_auth_info_list:
        raise http_exception_unauthorized(msg="Invalid API Key")

    valid_auth_info_list = [auth_info
                            for auth_info in api_auth_info_list
                            if bcrypt.checkpw(api_key.encode(), auth_info.hashed_key.encode())]
    if not valid_auth_info_list:
        raise http_exception_unauthorized(msg="Invalid API Key")

    return AuthInfo(identifier=valid_auth_info_list[0].identifier,
                    tenant_id=tenant_info.identifier)
