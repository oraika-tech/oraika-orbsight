from typing import Optional, List
from uuid import UUID

from cachetools import TTLCache, cached
from pandas import DataFrame
from sqlmodel import Field as SqlField
from sqlmodel import Session, SQLModel

from analyzer.model.data_store_request import DBStoreRequest
from .base_entity_manager import BaseEntityManager


class ProcessedDataEntity(SQLModel, table=True):
    __tablename__ = "insight_processed_data"

    identifier: Optional[int] = SqlField(default=None, primary_key=True)
    raw_data_id: int
    # Extraction from Text
    taxonomy_tags: List[str]
    taxonomy_terms: List[str]
    # Extraction from AI model
    emotion: str
    categories: List[str]
    # Text Features
    text_length: int
    text_lang: str
    # To store some comment or un categories info
    remark: str
    is_deleted: bool = SqlField(default=False)

    @staticmethod
    def convert_to_entity(data_request: DBStoreRequest):
        return ProcessedDataEntity(
            raw_data_id=data_request.raw_data_identifier,
            taxonomy_tags=data_request.structured_data.tags or [],
            taxonomy_terms=data_request.structured_data.terms or [],
            emotion=data_request.structured_data.emotion,
            categories=data_request.structured_data.categories or [],
            text_length=data_request.structured_data.text_length,
            text_lang=data_request.structured_data.text_language,
            remark=data_request.structured_data.remark,
        )


class TaxonomyEntity(SQLModel, table=True):
    __tablename__ = "config_taxonomy"

    identifier: UUID = SqlField(primary_key=True)
    keyword: str
    term: str
    tags: Optional[List[str]] = SqlField(default='[]')
    is_deleted: bool
    is_enabled: bool

    def as_dict(self):
        return {
            "keyword": self.keyword,
            "term": self.term,
            "tags": ",".join(self.tags)
        }


class CategoryEntity(SQLModel, table=True):
    __tablename__ = "config_category"

    identifier: UUID = SqlField(primary_key=True)
    name: str
    is_deleted: bool
    is_enabled: bool


class DBEntityManager(BaseEntityManager):

    def hash_key(self, tenant_id: UUID):
        return tenant_id

    def _snake_case(self, string: str, sep: str = ' ') -> str:
        words = [split_str.strip() for split_str in string.split(sep)]
        return "_".join(words)

    # Keeping it to less than equal to cron period. Main idea that at least it can handle single burst of events
    @cached(cache=TTLCache(maxsize=32, ttl=300), key=hash_key)
    def get_taxonomy_dataframe(self, tenant_id: UUID) -> DataFrame:
        with Session(self._get_tenant_engine(tenant_id)) as session:
            taxonomy_entities = session.query(TaxonomyEntity).filter(
                TaxonomyEntity.is_deleted == False,
                TaxonomyEntity.is_enabled == True,
            )
            if taxonomy_entities is not None:
                return DataFrame(
                    [taxonomy_entity.as_dict() for taxonomy_entity in taxonomy_entities]
                ).convert_dtypes().apply(lambda col: col.str.lower())

            return DataFrame()

    @cached(cache=TTLCache(maxsize=32, ttl=300), key=hash_key)
    def get_categories(self, tenant_id: UUID) -> List[str]:
        with Session(self._get_tenant_engine(tenant_id)) as session:
            category_entities = session.query(CategoryEntity).filter(
                CategoryEntity.is_deleted == False,
                CategoryEntity.is_enabled == True,
            )
            if category_entities is not None:
                return [category_entity.name for category_entity in category_entities]
            return []

    def insert_structured_data(self, data_request: DBStoreRequest) -> int:
        data_entity = ProcessedDataEntity.convert_to_entity(data_request)
        with Session(self._get_tenant_engine(data_request.tenant_id)) as session:
            session.add(data_entity)
            session.commit()
            session.refresh(data_entity)
            return data_entity.identifier
