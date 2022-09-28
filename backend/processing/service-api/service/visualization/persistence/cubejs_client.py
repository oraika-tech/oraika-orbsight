import logging
from typing import Optional, List, Any, Dict

import requests
from jose import jwt
from pydantic import BaseSettings, PrivateAttr, BaseModel

from service.visualization.domain.model.chart_models import FilterDO
from ...common.settings import settings
from ...common.utils import to_camel_case

logger = logging.getLogger(__name__)


class FilterCubeJs(BaseModel):
    member: str
    values: List[str]
    operator: Optional[str]


class CubejsClient(BaseSettings):
    _headers: Dict[str, Any] = PrivateAttr()
    _cubejs_operators = PrivateAttr()
    _filter_field_name = PrivateAttr()
    endpoint: Optional[str] = settings.CUBEJS_API_ENDPOINT
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
        self._filter_field_name = {
            'category': 'Categories.category',
            'taxonomy': 'TaxonomyTags.taxonomyTag',
            'term': 'TaxonomyTerms.taxonomyTerm',
            'emotion': 'ProcessedDataViewV1.emotion',
            'observerType': 'ProcessedDataViewV1.observerType',
            'observer': 'ProcessedDataViewV1.observerName',
            'entity': 'ProcessedDataViewV1.entityName',
            'lang': 'ProcessedDataViewV1.textLang',
            'author': 'ProcessedDataViewV1.authorName'
        }

    def get_token(self, tenant_code: str):
        if tenant_code not in self.tenant_tokens:
            self.tenant_tokens[tenant_code] = jwt.encode({"tenantCode": tenant_code},
                                                         settings.CUBEJS_SECRET_KEY,
                                                         algorithm=settings.ALGORITHM)
        return self.tenant_tokens[tenant_code]

    def update_cubejs_fields(self, filter_list: List[FilterDO]):
        for filter_obj in filter_list:
            opr = filter_obj.operator if filter_obj.operator else '='
            filter_obj.operator = self._cubejs_operators.get(opr)
            if filter_obj.name in self._filter_field_name:
                filter_obj.name = self._filter_field_name[filter_obj.name]
            else:
                filter_obj.name += "Name"
                filter_obj.name = "ProcessedDataViewV1." + to_camel_case(filter_obj.name)

    @staticmethod
    def get_query_with_filter(query: dict, filter_list: List[FilterCubeJs]):
        query["filters"] = [filter_obj.dict() for filter_obj in filter_list]
        return query

    def fetch_data(self, tenant_code: str, query: dict, filter_list: List[FilterDO]) -> List[dict]:
        filters = [FilterCubeJs(member=filterDO.name, values=filterDO.values, operator=filterDO.operator)
                   for filterDO in filter_list]
        try:
            self._headers["authorization"] = "Bearer {}".format(self.get_token(tenant_code))
            if filters:
                query = self.get_query_with_filter(query, filters)
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
