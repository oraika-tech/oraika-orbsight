from abc import ABC
from datetime import datetime
from typing import List, Any

import dateparser
from obsei.source.base_source import BaseSource

from service.common.utils.utils import hash_text
from service.workflow.nodes.observer.executor.base_executor import BaseObserverExecutor, ObserverType, ObserverJobData, SourceConfig, SourceResponse
from service.workflow.nodes.observer.observer_client import GoogleNewsOutscraperClient, GoogleNewsOutscraperConfig, GoogleSearchOutscraperClient, \
    GoogleSearchOutscraperConfig, GoogleNewsResult, GoogleSearchOutscraperResult


class BaseOutscraperExecutor(BaseObserverExecutor, ABC):

    def convert_id_column(self, id_column: Any):
        return hash_text(id_column)


class GoogleNewsOutscraperExecutor(BaseOutscraperExecutor):
    type: ObserverType = ObserverType.GoogleNews
    is_obsei_client: bool = False
    default_source_config: SourceConfig = SourceConfig(lookup_period='5m', limit_count=10)
    source: BaseSource = GoogleNewsOutscraperClient()
    drop_id_column: bool = False
    id_column: str = 'link'
    time_column: str = 'datetime'
    drop_columns: List[str] = ['description']

    def get_config(self, event: ObserverJobData, config: SourceConfig):
        return GoogleNewsOutscraperConfig(
            query=event.query,
            tbs=event.tbs,
            pages_per_query=event.number_of_pages or 1,
            language='en',
            region=None
        )

    def convert_date_column(self, date_value: str):
        return dateparser.parse(date_value)

    def create_source_response(self, responses: list[GoogleNewsResult]) -> list[SourceResponse]:
        return [
            SourceResponse(
                reference_id=self.convert_id_column(response.link),
                raw_text=response.title + '\n' + response.body,
                event_time=self.convert_date_column(response.posted),
                data={
                    'query': response.query,
                    'position': response.position,
                    'posted': response.posted,
                    'source': response.source,
                    'link': response.link
                }
            )
            for response in responses
        ]


class GoogleSearchOutscraperExecutor(BaseOutscraperExecutor):
    type: ObserverType = ObserverType.GoogleSearch
    is_obsei_client: bool = False
    default_source_config: SourceConfig = SourceConfig(lookup_period='5m', limit_count=10)
    source: BaseSource = GoogleSearchOutscraperClient()
    drop_id_column: bool = False
    id_column: str = 'link'
    time_column: str = 'datetime'
    drop_columns: List[str] = ['description']

    def get_config(self, event: ObserverJobData, config: SourceConfig):
        return GoogleSearchOutscraperConfig(
            query=event.query,
            pages_per_query=event.number_of_pages or 1,
            language='en',
            region=None
        )

    def create_source_response(self, responses: list[GoogleSearchOutscraperResult]) -> list[SourceResponse]:
        event_time = datetime.now()
        return [
            SourceResponse(
                reference_id=self.convert_id_column(organic_result.link),
                raw_text=organic_result.title + '\n' + organic_result.description,
                event_time=event_time,
                data={'link': organic_result.link}
            )
            for response in responses
            for organic_result in response.organic_results
        ]
