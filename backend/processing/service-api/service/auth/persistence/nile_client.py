from typing import Any

import requests
from nile_api import AuthenticatedClient
from nile_api.api.users import validate_user, get_user
from nile_api.models import Token, User
from pydantic import BaseSettings, Field, PrivateAttr
from starlette import status

from service.auth.domain.model.cache_models import NileUser


class NileClient(BaseSettings):
    url: str = Field("https://prod.thenile.dev", env='NILE_URL')
    workspace_name: str = Field("oraika-prod", env='NILE_WORKSPACE')
    workspace_token: str = Field("", env='NILE_WS_TOKEN')
    _client: AuthenticatedClient = PrivateAttr()
    _validate_url: str = PrivateAttr()

    def __init__(self, **values: Any):
        super().__init__(**values)
        self._client = AuthenticatedClient(base_url=self.url, token=self.workspace_token)
        self._validate_url = self.url + "/workspaces/" + self.workspace_name + "/auth/validate"

    def validate_user_token(self, token: str) -> bool:
        headers = {
            "content-type": "application/json"
        }
        response = requests.request("POST", self._validate_url, json=Token(token=token).to_dict(), headers=headers)
        return response.status_code == status.HTTP_204_NO_CONTENT

    def validate_user_token_buggy(self, token: str):
        is_valid = validate_user.sync(
            workspace=self.workspace_name,
            client=self._client,
            json_body=Token(token=token)
        )

        return is_valid

    def get_user_info(self, user_id) -> NileUser:
        user: User = get_user.sync(
            workspace=self.workspace_name,
            client=self._client,
            id=user_id
        )
        return NileUser(
            id=user_id,
            email=user.email,
            name=user.metadata.additional_properties.get('name'),
            org_ids=list(user.org_memberships.to_dict().keys())
        )
