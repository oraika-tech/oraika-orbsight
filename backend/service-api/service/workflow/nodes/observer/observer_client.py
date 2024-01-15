import json
import os
from abc import ABC
from typing import Optional

from obsei.source.base_source import BaseSource, BaseSourceConfig
from outscraper import ApiClient
from pydantic import BaseModel

from service.common.models import TimeBasedSearch


class OutscraperClient(BaseSource, ABC):
    client: ApiClient = ApiClient(api_key=os.environ["OUTSCRAPPER_API_KEY"])


class GoogleSearchOutscraperConfig(BaseSourceConfig):
    TYPE: str = "GoogleSearch"
    query: str
    pages_per_query: Optional[int] = 1
    language: Optional[str] = 'en'
    region: Optional[str] = None


class OrganicResult(BaseModel):
    title: str
    description: str
    link: str


class SearchInformation(BaseModel):
    total_results: int


class GoogleSearchOutscraperResult(BaseModel):
    query: str
    organic_results: list[OrganicResult]
    ads: Optional[list] = None
    shopping_results: Optional[list] = None
    related_questions: Optional[list] = None
    related_searches: Optional[list] = None
    knowledge_graph: Optional[dict] = None
    search_information: SearchInformation


class GoogleSearchOutscraperClient(OutscraperClient):

    def lookup(self, config: GoogleSearchOutscraperConfig, **kwargs):
        results = self.client.google_search(
            config.query,
            pages_per_query=config.pages_per_query,
            language=config.language,
            region=config.region,
            fields=['query', 'organic_results', 'search_information']
        )
        print("result: ", json.dumps(results))
        return [
            GoogleSearchOutscraperResult(**result)
            for result in results
        ]


class GoogleNewsOutscraperConfig(BaseSourceConfig):
    TYPE: str = "GoogleNews"
    query: str
    tbs: Optional[TimeBasedSearch] = None
    pages_per_query: Optional[int] = 1
    language: Optional[str] = 'en'
    region: Optional[str] = None


class GoogleNewsResult(BaseModel):
    query: str
    position: int
    title: str
    body: str
    posted: str
    source: str
    link: str


class GoogleNewsOutscraperClient(OutscraperClient):

    def lookup(self, config: GoogleNewsOutscraperConfig, **kwargs):
        results = self.client.google_search_news(
            config.query,
            tbs=config.tbs,
            pages_per_query=config.pages_per_query,
            language=config.language,
            region=config.region
        )
        return [
            GoogleNewsResult(**result)
            for records in results for result in records
        ]
