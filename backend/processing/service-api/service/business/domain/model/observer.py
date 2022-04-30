from typing import Optional

from pydantic import BaseModel


OBSERVER_TYPE = {
    1: "Twitter",
    2: "Android",
    3: "iOS"
}


class ObserverData(BaseModel):
    official_handle: Optional[str]
    url: Optional[str]


class ObserverInfo(BaseModel):
    identifier: Optional[int]
    name: str
    observer_type: str
    entity_id: int
    entity_name: str
    data: ObserverData
    is_enabled: bool
    company_id: Optional[int]

    def as_dict(self):
        return {
            'Identifier': self.identifier,
            'Name': self.name,
            'Type': self.observer_type,
            'Entity': self.entity_name,
            'Data Source': self.data.url if self.data.url else self.data.official_handle,
            'Enabled': self.is_enabled,
        }
