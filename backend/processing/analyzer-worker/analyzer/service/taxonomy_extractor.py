import ast
from typing import Dict, Set, Optional, Any, List, Union

from cachetools import TTLCache, cached
from pandas import DataFrame
from pydantic import Field, BaseSettings
from sqlalchemy import Column

from analyzer.model.taxonomy_data import TaxonomyData
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import Field as SqlField, Session, SQLModel, create_engine


class TaxonomyEntity(SQLModel, table=True):
    __tablename__ = "domain_dictionary"

    identifier: Optional[int] = SqlField(default=None, primary_key=True)
    company_id: int
    term: str
    categories: Optional[List[str]]
    data: Optional[Dict[str, Any]] = SqlField(default='{}', sa_column=Column(JSONB))
    is_deleted: bool

    def as_dict(self):
        return {
            "term": self.term,
            "categories": ",".join(self.categories),
            "data": str(self.data)
        }


class TaxonomyExtractor(BaseSettings):
    db_host: Optional[str] = Field("localhost:5432", env='DB_HOST')
    db_name: str = Field("obsights_business", env='CONFIG_DB_NAME')
    db_user: str = Field("obsights", env='CONFIG_DB_USER')
    db_password: str = Field("obsights", env='CONFIG_DB_PASSWORD')
    engine: Any

    def __init__(self, **data: Any):
        super().__init__(**data)
        connection_string = f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}/{self.db_name}"
        self.engine = create_engine(connection_string)

    def hash_key(self, company_id: int):
        return company_id

    # Keeping it to less than equal to cron period. Main idea that at least it can handle single burst of events
    @cached(cache=TTLCache(maxsize=32, ttl=300), key=hash_key)
    def get_taxonomy(self, company_id: int) -> DataFrame:
        with Session(self.engine) as session:
            domain_dictionary = session.query(TaxonomyEntity).filter(
                TaxonomyEntity.company_id == company_id,
                TaxonomyEntity.is_deleted == False,
            )
            if domain_dictionary is not None:
                return DataFrame(
                    [term.as_dict() for term in domain_dictionary]
                ).convert_dtypes().apply(lambda col: col.str.lower())

            return DataFrame()

    # Extract taxonomy data via keywords
    def extract_taxonomy(self, tokens: List[str], company_id: int) -> TaxonomyData:
        taxonomy_df = self.get_taxonomy(company_id)

        taxonomy_df['Search'] = taxonomy_df['term'].str.fullmatch('|'.join(tokens))
        keywords_present_df = taxonomy_df[taxonomy_df['Search'] == True]

        keywords_found = keywords_present_df.shape[0]

        if keywords_found > 0:
            categories: Set[str] = set()

            for categories_string in set(keywords_present_df['categories'].to_list()):
                if categories_string is not None and categories_string != "":
                    categories.update(categories_string.split(","))

            taxonomy_dict_list = []
            for taxonomy_dict_string in set(keywords_present_df['data'].to_list()):
                if taxonomy_dict_string is not None and taxonomy_dict_string != "" and taxonomy_dict_string != "{}":
                    taxonomy_dict_list.append(ast.literal_eval(taxonomy_dict_string))
            taxonomy_map = TaxonomyExtractor._merge_dicts(taxonomy_dict_list)

            return TaxonomyData(
                categories=categories,
                taxonomy_map=taxonomy_map
            )
        else:
            return TaxonomyData()

    @staticmethod
    def _merge_dicts(dicts: List[Dict[str, str]]) -> Dict[str, Union[Set[str], bool]]:
        merged_dict: Dict[str, Union[Set[str], bool]] = {}
        for dictionary in dicts:
            for key, value in dictionary.items():
                if key in merged_dict:
                    merged_dict[key].add(value)
                else:
                    merged_dict[key] = {value}
        return merged_dict
