from typing import Optional, List

from pydantic import BaseModel


class EntityInfo(BaseModel):
    identifier: Optional[int]
    name: str
    simple_name: str
    city: Optional[str]
    country: Optional[str]
    regulated_type: Optional[List[str]]
    is_enabled: bool
    is_deleted: bool
    company_id: int

    def as_dict(self):
        entity_type = self.regulated_type
        if self.regulated_type is None or len(self.regulated_type) == 0:
            entity_type = ["Unregulated"]
        return {
            'Identifier': self.identifier,
            'Name': self.simple_name,
            'Entity Type': ", ".join(entity_type),
            'Enabled': self.is_enabled,
        }
