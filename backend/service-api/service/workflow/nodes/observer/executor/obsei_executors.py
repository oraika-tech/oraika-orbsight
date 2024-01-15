import logging
from abc import ABC
from datetime import datetime
from typing import List, Optional, Any, Dict

import dateparser
from obsei.payload import TextPayload
from obsei.source.appstore_scrapper import AppStoreScrapperSource, AppStoreScrapperConfig
from obsei.source.base_source import BaseSource
from obsei.source.facebook_source import FacebookSource, FacebookSourceConfig, FacebookCredentials
from obsei.source.google_maps_reviews import OSGoogleMapsReviewsSource, OSGoogleMapsReviewsConfig
from obsei.source.google_news_source import GoogleNewsSource, GoogleNewsConfig
from obsei.source.playstore_scrapper import PlayStoreScrapperSource, PlayStoreScrapperConfig
from obsei.source.reddit_source import RedditSource, RedditConfig, RedditCredInfo
from obsei.source.twitter_source import TwitterSource, TwitterSourceConfig, TwitterCredentials
from pydantic import SecretStr, Field

from service.common.utils.dateutils import convert_to_local_time
from service.workflow.nodes.observer.executor.base_executor import BaseObserverExecutor, ObserverType, ObserverJobData, SourceConfig, SourceResponse

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class BaseObseiExecutor(BaseObserverExecutor, ABC):

    def create_source_response(self, responses: List[TextPayload]) -> list[SourceResponse]:
        obsei_response_list = []

        for source_response in responses:
            logger.error(f"source_response: {source_response}")
            reference_id = str(source_response.meta[self.id_column])
            event_time = source_response.meta[self.time_column]

            self.drop_unwanted_columns(source_response)

            obsei_response_list.append(SourceResponse(
                reference_id=self.convert_id_column(reference_id),
                raw_text=source_response.processed_text,
                event_time=self.convert_date_column(event_time),
                data=source_response.meta
            ))

        return obsei_response_list


class TwitterExecutor(BaseObseiExecutor):
    type: ObserverType = ObserverType.Twitter
    default_source_config: SourceConfig = SourceConfig(lookup_period='5m', limit_count=100)
    source: BaseSource = TwitterSource()
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


class PlayStoreExecutor(BaseObseiExecutor):
    type: ObserverType = ObserverType.Android
    default_source_config: SourceConfig = SourceConfig(lookup_period='5m', limit_count=10)
    source: BaseSource = PlayStoreScrapperSource()
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


class AppleStoreExecutor(BaseObseiExecutor):
    type: ObserverType = ObserverType.iOS
    default_source_config: SourceConfig = SourceConfig(lookup_period='5m', limit_count=450)
    source: BaseSource = AppStoreScrapperSource()
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


class GoogleMapsExecutor(BaseObseiExecutor):
    type: ObserverType = ObserverType.GoogleMaps
    api_key: Optional[SecretStr] = Field(None, alias="OUTSCRAPPER_API_KEY")
    default_source_config: SourceConfig = SourceConfig(lookup_period='5m', limit_count=100)
    source: BaseSource = OSGoogleMapsReviewsSource()
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


class FacebookExecutor(BaseObseiExecutor):
    # TODO: Test it before releasing to client
    type: ObserverType = ObserverType.Facebook
    default_source_config: SourceConfig = SourceConfig(lookup_period='5m', limit_count=100)
    source: BaseSource = FacebookSource()
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


class RedditExecutor(BaseObseiExecutor):
    # TODO: Test it before releasing to client
    type: ObserverType = ObserverType.Reddit
    default_source_config: SourceConfig = SourceConfig(lookup_period='5m', limit_count=100)
    source: BaseSource = RedditSource()
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


class GoogleNewsExecutor(BaseObseiExecutor):
    # TODO: Test it before releasing to client
    type: ObserverType = ObserverType.GoogleNews
    default_source_config: SourceConfig = SourceConfig(lookup_period='5m', limit_count=10)
    source: BaseSource = GoogleNewsSource()
    drop_id_column: bool = False
    id_column: str = 'link'
    time_column: str = 'datetime'
    drop_columns: List[str] = ['description']

    def get_config(self, event: ObserverJobData, config: SourceConfig):
        return GoogleNewsConfig(
            query=event.query,
            lookup_period=config.lookup_period,
            max_results=config.limit_count,
            language=event.language or "en",
            country=event.country,
            fetch_article=False
        )

    def convert_date_column(self, date_value: Any):
        if isinstance(date_value, datetime):
            return date_value
        # TODO how to fix if published date is null
        return datetime.now() if not date_value or str(date_value) == "" else dateparser.parse(date_value)

    def convert_id_column(self, id_column: Any):
        # extract google news article id from link
        # e.g. "news.google.com/articles/CBMiYWh0dHBztcmF0ZS1jdXQtdmlld3PSAQA?hl=en-IN&gl=IN&ceid=IN%3Aen"
        return id_column.split("/")[-1].split("?")[0]

    def drop_unwanted_columns(self, response: TextPayload):
        # Drop columns
        if self.drop_time_column:
            response.meta.pop(self.time_column, None)
        if self.drop_id_column:
            response.meta.pop(self.id_column, None)
        for column in self.drop_columns:
            response.meta.pop(column, None)

        # Drop publisher.keymap
        publisher_dict: Optional[Dict[str, Any]] = response.meta.pop('publisher', None)
        if publisher_dict:
            for k, v in publisher_dict.items():
                response.meta["publisher_" + k] = v
