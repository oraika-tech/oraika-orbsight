from typing import List

from pydantic import BaseModel


class UserInfo(BaseModel):
    company_id: int
    name: str
    employee_id: int
    user_id: int
    role_ids: List[int]

