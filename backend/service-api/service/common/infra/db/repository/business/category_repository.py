from typing import Optional, List
from uuid import UUID

from sqlalchemy import false
from sqlmodel import SQLModel, Field, Session, select

from service.common.infra.db.db_utils import get_tenant_engine


class CategoryEntity(SQLModel, table=True):
    __tablename__ = "config_category"

    identifier: Optional[UUID] = Field(default=None, primary_key=True)
    name: str
    is_enabled: bool
    is_deleted: bool


def get_all_category(tenant_id: UUID) -> List[CategoryEntity]:
    with Session(get_tenant_engine(tenant_id)) as session:
        return list(session.exec(select(CategoryEntity).where(
            CategoryEntity.is_deleted == false()
        )).all())
