from typing import Optional, List
from uuid import UUID

from sqlalchemy import false, true, Column, Text
from sqlalchemy.dialects.postgresql import ARRAY
from sqlmodel import SQLModel, Field, Session, select

from service.common.infra.db.db_utils import get_tenant_engine


class TaxonomyEntity(SQLModel, table=True):
    __tablename__ = "config_taxonomy"

    identifier: Optional[UUID] = Field(default=None, primary_key=True)
    term: str
    keyword: str
    description: Optional[str] = None
    tags: Optional[List[str]] = Field(default='{}', sa_column=Column(ARRAY(Text)))
    is_deleted: bool
    is_enabled: bool


def get_taxonomy_data(tenant_id: UUID) -> List[TaxonomyEntity]:
    with Session(get_tenant_engine(tenant_id)) as session:
        return list(session.exec(
            select(TaxonomyEntity)
            .where(TaxonomyEntity.is_deleted == false())
        ).all())


def get_taxonomies(tenant_id: UUID) -> list[TaxonomyEntity]:
    with Session(get_tenant_engine(tenant_id)) as session:
        return list(session.exec(
            select(TaxonomyEntity).where(
                TaxonomyEntity.is_deleted == false(),
                TaxonomyEntity.is_enabled == true()
            )
        ).all())
