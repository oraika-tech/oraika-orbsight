import logging
from typing import List, Any, Dict

import requests
from jose import jwt

from service.common.config.app_settings import app_settings

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

endpoint: str = app_settings.CUBEJS_API_ENDPOINT
tenant_tokens: Dict[str, str] = {}

_headers: Dict[str, Any] = {
    "content-type": "application/json",
}

_cubejs_operators = {
    '=': 'equals',
    'in': 'equals',
    'range': 'inDateRange',
    '>': 'afterDate',
    '<': 'beforeDate'
}


def get_token(tenant_code: str):
    if tenant_code not in tenant_tokens:
        tenant_tokens[tenant_code] = jwt.encode({"tenantCode": tenant_code},
                                                app_settings.CUBEJS_SECRET_KEY,
                                                algorithm=app_settings.ALGORITHM)
    return tenant_tokens[tenant_code]


def get_cubejs_filter_from_domain(filter_obj: dict):
    member = filter_obj.get('name', filter_obj['member'])
    values = filter_obj.get('values')
    operator = _cubejs_operators.get(filter_obj.get('operator') or '=', filter_obj.get('operator'))
    if not filter_obj.get('values'):
        return {"member": member, "operator": operator}
    else:
        return {"member": member, "values": values, "operator": operator}


def get_cubejs_filter_list(filter_list: List[dict]):
    logger.debug("Filter_list: %s", filter_list)
    return [get_cubejs_filter_from_domain(filter_obj) for filter_obj in filter_list]


def fetch_cubejs_data(tenant_code: str, query: dict) -> List[dict]:
    try:
        if 'filters' in query:
            query['filters'] = get_cubejs_filter_list(query['filters'])

        _headers["authorization"] = "Bearer {}".format(get_token(tenant_code))
        response = requests.request("POST", endpoint, json={'query': query}, headers=_headers, timeout=5)

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
