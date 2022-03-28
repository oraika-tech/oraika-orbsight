from typing import Union, Set, Dict, List, Optional

from pydantic import BaseModel


class ObserverInfo(BaseModel):
    identifier: int
    name: str
    type: str


class EntityInfo(BaseModel):
    identifier: int
    simple_name: str
    type: str
    country: Optional[str]
    city: Optional[str]


class DBStoreRequest(BaseModel):
    structured_data: Dict[str, Union[str, Set[str], bool, int]]
    raw_data_identifier: int
    company_id: int
    observer_info: ObserverInfo
    entity_info: EntityInfo

    def get_structured_data_of_list_type(self, key: str, default: Optional[List[str]] = None) -> Optional[List[str]]:
        value = self.structured_data.get(key, None)
        return list(value) if value and isinstance(value, Set) else default

    def get_structured_data_of_str_type(self, key: str, default: Optional[str] = None) -> Optional[str]:
        value = self.structured_data.get(key, None)
        return value if value and isinstance(value, str) else default

    def get_structured_data_of_int_type(self, key: str, default: Optional[int] = None) -> Optional[int]:
        value = self.structured_data.get(key, None)
        return value if value and isinstance(value, int) else default

    def get_structured_data_of_bool_type(self, key: str, default: Optional[bool] = None) -> Optional[bool]:
        value = self.structured_data.get(key, None)
        return value if value and isinstance(value, bool) else default
