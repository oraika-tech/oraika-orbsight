import logging
from abc import abstractmethod
from datetime import datetime
from enum import Enum
from typing import List, Any, Optional, Dict
from uuid import UUID

from obsei.payload import TextPayload
from obsei.source.base_source import BaseSource
from pydantic import BaseModel
from pydantic_settings import BaseSettings

from service.common.models import TimeBasedSearch
from service.common.utils.dateutils import convert_to_local_time

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class ObserverType(int, Enum):
    Twitter = 1
    Android = 2
    iOS = 3
    GoogleMaps = 4
    Facebook = 5
    Reddit = 6
    GoogleNews = 7
    GoogleSearch = 8


class ObserverJobData(BaseModel):
    tenant_id: UUID
    observer_id: UUID
    observer_type: ObserverType
    url: Optional[str] = None
    query: Optional[str] = None
    country: Optional[str] = None
    language: Optional[str] = None
    page_id: Optional[str] = None
    number_of_pages: Optional[int] = None
    subreddit: Optional[str] = None
    lookup_period: Optional[str] = None
    limit_count: Optional[int] = None
    tbs: Optional[TimeBasedSearch] = None


class SourceConfig(BaseModel):
    lookup_period: str = '5m'
    limit_count: int = 100


class SourceResponse(BaseModel):
    reference_id: str
    parent_reference_id: Optional[str] = None
    raw_text: str
    event_time: datetime
    data: Optional[Dict[str, Any]] = None


class BaseObserverExecutor(BaseSettings):
    type: ObserverType

    is_obsei_client: bool = True
    default_source_config: SourceConfig
    source: BaseSource
    drop_id_column: bool = True
    id_column: str
    drop_time_column: bool = True
    time_column: str
    drop_columns: List[str] = []

    @abstractmethod
    def get_config(self, event: ObserverJobData, config: SourceConfig):
        pass

    def convert_date_column(self, date_value: Any):
        return convert_to_local_time(date_value)

    def convert_id_column(self, id_value: Any):
        return id_value

    def get_secret_config(self, event: ObserverJobData):
        pass

    def create_source_response(self, responses: list) -> list[SourceResponse]:
        raise NotImplementedError()

    def fetch_data(self, event: ObserverJobData, config: Optional[SourceConfig] = None) -> List[SourceResponse]:
        source_config = self.get_config(event, config or self.default_source_config)
        logger.info(f"Source config: {source_config}")
        responses = self.source.lookup(source_config)
        logger.info(f"Source response: {responses}")
        return self.create_source_response(responses)

    def drop_unwanted_columns(self, response: TextPayload):
        # Drop columns
        if self.drop_time_column:
            response.meta.pop(self.time_column, None)
        if self.drop_id_column:
            response.meta.pop(self.id_column, None)
        for column in self.drop_columns:
            response.meta.pop(column, None)
