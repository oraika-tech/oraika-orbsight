import ast
from typing import Dict, Set, Optional, Any, List, Union

import pandas as pd
from pandas import DataFrame
from pydantic import Field, BaseSettings

from analyzer.model.entity_data import EntityData


class EntityExtractor(BaseSettings):
    keywords_df: Optional[DataFrame] = None
    keywords_data_source_type: str = Field("tsv")
    keywords_data_source: str = Field(r'rbi_keywords.tsv', env="KEYWORDS_DATA_SOURCE")

    def __init__(self, **data: Any):
        super().__init__(**data)

        if self.keywords_df is None:
            if self.keywords_data_source_type == "tsv":
                self.keywords_df = pd.read_csv(
                    self.keywords_data_source, sep='\t'
                ).convert_dtypes().apply(lambda col: col.str.lower())
                self.keywords_df = self.keywords_df.fillna('')
            else:
                self.keywords_df = DataFrame()

    # Extract entities via keywords
    def extract_entities(self, tokens: List[str], entity_owner_id: int) -> EntityData:
        # TODO: use entity_owner_id to fetch correct entity, domain and keywords data from DB

        # TODO: test in multi process environment, ideally it will work
        # Otherwise loading part in can be moved to extract_entities function from constructor
        self.keywords_df['Search'] = self.keywords_df['Name'].str.fullmatch('|'.join(tokens))
        keywords_present_df = self.keywords_df[self.keywords_df['Search'] == True]

        keywords_found = keywords_present_df.shape[0]

        if keywords_found > 0:
            tags: Set[str] = set()
            categories: Set[str] = set()

            for tags_string in set(keywords_present_df['Tags'].to_list()):
                if tags_string is not None and tags_string != "":
                    tags.update(tags_string.split(","))

            for categories_string in set(keywords_present_df['Categories'].to_list()):
                if categories_string is not None and categories_string != "":
                    categories.update(categories_string.split(","))

            entity_dict_list = []
            for entity_dict_string in set(keywords_present_df['Entity Map'].to_list()):
                if entity_dict_string is not None and entity_dict_string != "" and entity_dict_string != "{}":
                    entity_dict_list.append(ast.literal_eval(entity_dict_string))
            entity_map = EntityExtractor._merge_dicts(entity_dict_list)

            return EntityData(
                tags=tags,
                categories=categories,
                entity_map=entity_map
            )
        else:
            return EntityData()

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
