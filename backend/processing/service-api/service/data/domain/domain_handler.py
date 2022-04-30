from datetime import datetime, date
from typing import Union, List, Optional

from pydantic import BaseSettings
from .base import BasePersistenceManager
from .model.processed_data import ProcessedDataInfo


class DataDomainHandler(BaseSettings):
    persistence_manager: BasePersistenceManager

    def get_processed_data_with_raw_data(
        self,
        company_id: int,
        start_date: Union[datetime, date],
        end_date: Union[datetime, date],
        text_lang: str = 'en',
        entity_name: str = 'All',
        observer_type: str = 'All'
    ) -> Optional[List[ProcessedDataInfo]]:
        return self.persistence_manager.get_processed_data_with_raw_data(
            company_id=company_id,
            start_date=start_date,
            end_date=end_date,
            text_lang=text_lang,
            entity_name=entity_name,
            observer_type=observer_type
        )

    def get_distinct_entity_names(self, company_id: int) -> Optional[List[str]]:
        return self.persistence_manager.get_distinct_entity_names(company_id)

    def get_distinct_observer_types(self, company_id: int) -> Optional[List[str]]:
        return self.persistence_manager.get_distinct_observer_types(company_id)
