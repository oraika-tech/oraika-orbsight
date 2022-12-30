import logging
from typing import List, Any, Dict

import requests
from jose import jwt
from pydantic import BaseSettings, PrivateAttr

from ...common.settings import settings

logger = logging.getLogger(__name__)


class CubejsClient(BaseSettings):
    _headers: Dict[str, Any] = PrivateAttr()
    _cubejs_operators = PrivateAttr()
    endpoint: str = settings.CUBEJS_API_ENDPOINT
    tenant_tokens: Dict[str, str] = {}

    def __init__(self, **data: Any):
        super().__init__(**data)

        self._headers = {
            "content-type": "application/json",
        }
        self._cubejs_operators = {
            '=': 'equals',
            'in': 'equals',
            'range': 'inDateRange',
            '>': 'afterDate',
            '<': 'beforeDate'
        }

    def get_token(self, tenant_code: str):
        if tenant_code not in self.tenant_tokens:
            self.tenant_tokens[tenant_code] = jwt.encode({"tenantCode": tenant_code},
                                                         settings.CUBEJS_SECRET_KEY,
                                                         algorithm=settings.ALGORITHM)
        return self.tenant_tokens[tenant_code]

    def get_cubejs_filter_from_domain(self, filter_obj: dict):
        member = filter_obj.get('name', filter_obj['member'])
        values = filter_obj.get('values')
        operator = self._cubejs_operators.get(filter_obj.get('operator') or '=', filter_obj.get('operator'))
        if filter_obj.get('values') is None:
            return {"member": member, "operator": operator}
        else:
            return {"member": member, "values": values, "operator": operator}

    def get_cubejs_filter_list(self, filter_list: List[dict]):
        logger.debug("Filter_list: %s", filter_list)
        return [self.get_cubejs_filter_from_domain(filter_obj) for filter_obj in filter_list]

    def fetch_data(self, tenant_code: str, query: dict) -> List[dict]:
        try:
            if 'filters' in query:
                query['filters'] = self.get_cubejs_filter_list(query['filters'])

            self._headers["authorization"] = "Bearer {}".format(self.get_token(tenant_code))
            response = requests.request("POST", self.endpoint, json={'query': query}, headers=self._headers, timeout=5)

            if response.status_code == 200:
                json_response = response.json()
                return json_response["data"]
            else:
                logging.error("Cubejs API failed Status:%d Response:%s Query:%s",
                              response.status_code, response.text, query)

            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise e
        except Exception as ex:
            raise RuntimeError(f"Cubejs API Exception: {ex}")

        return []
