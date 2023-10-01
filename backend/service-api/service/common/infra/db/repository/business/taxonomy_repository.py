from typing import Optional, List
from uuid import UUID

from sqlalchemy import false, true
from sqlmodel import SQLModel, Field as SqlField, Session

from service.common.infra.db.db_utils import get_tenant_engine


class TaxonomyEntity(SQLModel, table=True):
    __tablename__ = "config_taxonomy"

    identifier: Optional[UUID] = SqlField(default=None, primary_key=True)
    term: str
    keyword: str
    description: Optional[str]
    tags: Optional[List[str]]
    is_deleted: bool
    is_enabled: bool


def get_taxonomy_data(tenant_id: UUID) -> List[TaxonomyEntity]:
    with Session(get_tenant_engine(tenant_id)) as session:
        return session.query(TaxonomyEntity).filter(
            TaxonomyEntity.is_deleted == false()
        ).all()


def get_taxonomies(tenant_id: UUID) -> list[TaxonomyEntity]:
    with Session(get_tenant_engine(tenant_id)) as session:
        return session.query(TaxonomyEntity).filter(
            TaxonomyEntity.is_deleted == false(),
            TaxonomyEntity.is_enabled == true()
        ).all()
