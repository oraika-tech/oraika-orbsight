from pydantic import BaseModel


class UnstructuredDataRequest(BaseModel):
    company_id: int
    raw_text: str
