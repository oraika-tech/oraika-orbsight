from pydantic import BaseModel


class DashboardData(BaseModel):
    title: str
    link: str
