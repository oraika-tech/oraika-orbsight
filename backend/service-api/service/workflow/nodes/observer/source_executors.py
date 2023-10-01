import logging
from abc import abstractmethod
from datetime import datetime
from enum import Enum
from typing import Optional, Dict, Any, List
from uuid import UUID

import dateparser
import mmh3
from obsei.payload import TextPayload
from obsei.source.appstore_scrapper import AppStoreScrapperSource, AppStoreScrapperConfig
from obsei.source.base_source import BaseSource
from obsei.source.facebook_source import FacebookSource, FacebookSourceConfig, FacebookCredentials
from obsei.source.google_maps_reviews import OSGoogleMapsReviewsSource, OSGoogleMapsReviewsConfig
from obsei.source.google_news_source import GoogleNewsSource, GoogleNewsConfig
from obsei.source.playstore_scrapper import PlayStoreScrapperConfig, PlayStoreScrapperSource
from obsei.source.reddit_source import RedditSource, RedditConfig, RedditCredInfo
from obsei.source.twitter_source import TwitterSource, TwitterSourceConfig, TwitterCredentials
from pydantic import BaseModel, BaseSettings, SecretStr, Field

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


class ObserverJobData(BaseModel):
    tenant_id: UUID
    observer_id: UUID
    observer_type: ObserverType  # - app | twitter
    url: Optional[str]
    query: Optional[str]
    country: Optional[str]
    language: Optional[str]
    page_id: Optional[str]
    subreddit: Optional[str]
    lookup_period: Optional[str]
    limit_count: Optional[int]


class SourceConfig(BaseModel):
    lookup_period: str = '5m'
    limit_count: int = 100


class ObseiResponse(BaseModel):
    reference_id: str
    parent_reference_id: Optional[str]
    raw_text: str
    event_time: datetime
    data: Optional[Dict[str, Any]]


class BaseObserverExecutor(BaseSettings):
    type: ObserverType
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

    def fetch_data(self, event: ObserverJobData, config: Optional[SourceConfig] = None) -> List[ObseiResponse]:
        source_config = self.get_config(event, config or self.default_source_config)
        responses = self.source.lookup(source_config)
        return self.create_obsei_response(responses)

    def create_obsei_response(self, responses: List[TextPayload]):
        obsei_response_list = []

        for source_response in responses:
            reference_id = str(source_response.meta[self.id_column])
            event_time = source_response.meta[self.time_column]

            self.drop_unwanted_columns(source_response)

            obsei_response_list.append(ObseiResponse(
                reference_id=self.convert_id_column(reference_id),
                raw_text=source_response.processed_text,
                event_time=self.convert_date_column(event_time),
                data=source_response.meta
            ))

        return obsei_response_list

    def drop_unwanted_columns(self, response: TextPayload):
        # Drop columns
        if self.drop_time_column:
            response.meta.pop(self.time_column, None)
        if self.drop_id_column:
            response.meta.pop(self.id_column, None)
        for column in self.drop_columns:
            response.meta.pop(column, None)


class TwitterExecutor(BaseObserverExecutor):
    type = ObserverType.Twitter
    default_source_config: SourceConfig = SourceConfig(lookup_period='5m', limit_count=100)
    source = TwitterSource()
    id_column: str = 'id'
    time_column: str = 'created_at'
    drop_columns: List[str] = ['text']

    def get_config(self, event: ObserverJobData, config: SourceConfig):
        return TwitterSourceConfig(
            # Searching tweets tagging handle, it should not be retweet and not by handle itself
            # For example: @theofficialsbi -is:retweet -from:theofficialsbi
            query=event.query,
            tweet_fields=["conversation_id", "created_at", "id", "public_metrics", "text"],  # author_id
            user_fields=["id", "name", "public_metrics", "username", "verified"],
            expansions=["author_id"],
            place_fields=None,
            lookup_period=config.lookup_period,
            max_tweets=config.limit_count,
            cred_info=self.get_secret_config(event)
        )

    def get_secret_config(self, event: ObserverJobData):
        # Add a way to fetch credentials with tenant id and observer id
        return TwitterCredentials()


class PlayStoreExecutor(BaseObserverExecutor):
    type = ObserverType.Android
    default_source_config: SourceConfig = SourceConfig(lookup_period='5m', limit_count=10)
    source = PlayStoreScrapperSource()
    id_column: str = 'reviewId'
    time_column: str = 'at'
    drop_columns: List[str] = ['content']

    def get_config(self, event: ObserverJobData, config: SourceConfig):
        return PlayStoreScrapperConfig(
            app_url=event.url,
            lookup_period=config.lookup_period,
            max_count=config.limit_count,
            language=event.language,
            countries=[event.country] if event.country else None
        )


class AppleStoreExecutor(BaseObserverExecutor):
    type = ObserverType.iOS
    default_source_config: SourceConfig = SourceConfig(lookup_period='5m', limit_count=450)
    source = AppStoreScrapperSource()
    id_column: str = 'id'
    time_column: str = 'date'
    drop_columns: List[str] = ['content']

    def get_config(self, event: ObserverJobData, config: SourceConfig):
        return AppStoreScrapperConfig(
            app_url=event.url,
            lookup_period=config.lookup_period,
            max_count=config.limit_count,
            countries=[event.country] if event.country else None
        )


class GoogleMapsExecutor(BaseObserverExecutor):
    type = ObserverType.GoogleMaps
    api_key: Optional[SecretStr] = Field(None, env="OUTSCRAPPER_API_KEY")
    default_source_config: SourceConfig = SourceConfig(lookup_period='5m', limit_count=100)
    source = OSGoogleMapsReviewsSource()
    id_column: str = 'review_id'
    time_column: str = 'review_timestamp'
    drop_columns: List[str] = ['review_text', 'google_id', 'author_link', 'author_image', 'author_img_url',
                               'review_datetime_utc', 'reviews_id', 'review_img_url']

    def get_config(self, event: ObserverJobData, config: SourceConfig):
        return OSGoogleMapsReviewsConfig(
            queries=[event.url],
            lookup_period=config.lookup_period,
            number_of_reviews=config.limit_count,
            api_key=self.get_secret_config(event),
            country=event.country,
            language=event.language or 'en',  # TODO fix this in Obsei
        )

    def convert_date_column(self, date_value: Any):
        return convert_to_local_time(int(date_value))

    def get_secret_config(self, event: ObserverJobData):
        if not self.api_key:
            return None
        return self.api_key.get_secret_value()


class FacebookExecutor(BaseObserverExecutor):
    # TODO: Test it before releasing to client
    type = ObserverType.Facebook
    default_source_config: SourceConfig = SourceConfig(lookup_period='5m', limit_count=100)
    source = FacebookSource()
    id_column: str = 'id'
    time_column: str = 'created_time'
    drop_columns: List[str] = ['message']

    def get_config(self, event: ObserverJobData, config: SourceConfig):
        return FacebookSourceConfig(
            page_id=event.page_id,
            lookup_period=config.lookup_period,
            max_post=config.limit_count,
            cred_info=self.get_secret_config(event)
        )

    def get_secret_config(self, event: ObserverJobData):
        # Add a way to fetch credentials with tenant id and observer id
        return FacebookCredentials()


class RedditExecutor(BaseObserverExecutor):
    # TODO: Test it before releasing to client
    type = ObserverType.Reddit
    default_source_config: SourceConfig = SourceConfig(lookup_period='5m', limit_count=100)
    source = RedditSource()
    id_column: str = 'id'
    time_column: str = 'created_utc'
    drop_columns: List[str] = ['body_html']

    def get_config(self, event: ObserverJobData, config: SourceConfig):
        return RedditConfig(
            subreddits=[event.subreddit],
            lookup_period=config.lookup_period,
            cred_info=self.get_secret_config(event),
            include_post_meta=False
        )

    def convert_date_column(self, date_value: Any):
        return datetime.utcfromtimestamp(int(date_value))

    def get_secret_config(self, event: ObserverJobData):
        # Add a way to fetch credentials with tenant id and observer id
        return RedditCredInfo()


class GoogleNewsExecutor(BaseObserverExecutor):
    # TODO: Test it before releasing to client
    type = ObserverType.Reddit
    default_source_config: SourceConfig = SourceConfig(lookup_period='5m', limit_count=10)
    source = GoogleNewsSource()
    drop_id_column: bool = False
    id_column: str = 'url'
    time_column: str = 'published date'
    drop_columns: List[str] = ['description']

    def get_config(self, event: ObserverJobData, config: SourceConfig):
        return GoogleNewsConfig(
            query=event.query,
            lookup_period=config.lookup_period,
            max_results=config.limit_count,
            language=event.language,
            country=event.country,
            fetch_article=False
        )

    def convert_date_column(self, date_value: Any):
        # TODO how to fix if published date is null
        return datetime.now() if not date_value or str(date_value) == "" else dateparser.parse(date_value)

    def convert_id_column(self, id_column: Any):
        return "{:02x}".format(mmh3.hash(id_column, signed=False))

    def drop_unwanted_columns(self, response: TextPayload):
        # Drop columns
        if self.drop_time_column:
            response.meta.pop(self.time_column, None)
        if self.drop_id_column:
            response.meta.pop(self.id_column, None)
        for column in self.drop_columns:
            response.meta.pop(column, None)

        # Drop publisher.keymap
        publisher_dict: Dict[str, Any] = response.meta.pop('publisher', None)
        if publisher_dict:
            for k, v in publisher_dict.items():
                response.meta["publisher_" + k] = v
