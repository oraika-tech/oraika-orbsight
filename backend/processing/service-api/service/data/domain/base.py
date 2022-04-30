from abc import abstractmethod
from datetime import datetime, date, time
from typing import List, Optional, Union

from pydantic import BaseSettings
from .model.processed_data import ProcessedDataInfo


class BasePersistenceManager(BaseSettings):

    @abstractmethod
    def get_processed_data_with_raw_data(
            self,
            company_id: int,
            start_date: Union[datetime, date, time],
            end_date: Union[datetime, date, time],
            text_lang: str = 'en',
            entity_name: str = 'All',
            observer_type: str = 'All'
    ) -> Optional[List[ProcessedDataInfo]]:
        pass

    @abstractmethod
    def get_distinct_entity_names(self, company_id: int) -> Optional[List[str]]:
        pass

    @abstractmethod
    def get_distinct_observer_types(self, company_id: int) -> Optional[List[str]]:
        pass
