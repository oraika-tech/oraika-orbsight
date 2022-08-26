from datetime import datetime
from typing import Optional, Dict, Any, List

from obsei.source.twitter_source import TwitterSourceConfig, TwitterSource, TwitterCredentials
from obsei.source.appstore_scrapper import AppStoreScrapperConfig, AppStoreScrapperSource
from obsei.source.playstore_scrapper import PlayStoreScrapperConfig, PlayStoreScrapperSource
from pydantic import BaseModel, BaseSettings


class SourceConfig(BaseModel):
    lookup_period: str = '5m'
    limit_count: int = 100


class ObseiClientConfig(BaseModel):
    twitter_config: SourceConfig = SourceConfig()
    android_config: SourceConfig = SourceConfig()
    ios_config: SourceConfig = SourceConfig()


class ObseiResponse(BaseModel):
    reference_id: str
    parent_reference_id: Optional[str]
    raw_text: str
    event_time: datetime
    data: Optional[Dict[str, Any]]


class ObseiClient(BaseSettings):
    source_playstore = PlayStoreScrapperSource()
    source_appstore = AppStoreScrapperSource()
    source_twitter = TwitterSource()
    config: ObseiClientConfig = ObseiClientConfig()

    def __init__(self, config: ObseiClientConfig, **values: Any):
        super().__init__(**values)
        self.config = config

    @staticmethod
    def get_source_config(default_config: SourceConfig, config: Optional[SourceConfig] = None):
        return default_config if config is None else config

    def get_twitter_config(self, query, config):
        config = self.get_source_config(self.config.twitter_config, config)
        return TwitterSourceConfig(
            # Searching tweets tagging handle, it should not be retweet and not by handle itself
            # For example: @theofficialsbi -is:retweet -from:theofficialsbi
            query=f'@{query} -is:retweet -from:{query}',
            tweet_fields=["conversation_id", "created_at", "id", "public_metrics", "text"],  # author_id
            user_fields=["id", "name", "public_metrics", "username", "verified"],
            expansions=["author_id"],
            place_fields=None,
            lookup_period=config.lookup_period,
            max_tweets=config.limit_count,
            cred_info=TwitterCredentials()
        )

    def fetch_twitter_data(self, query, config: Optional[SourceConfig] = None):
        source_config = self.get_twitter_config(query, config)
        source_response_list = self.source_twitter.lookup(source_config)
        return self._create_obsei_response(source_response_list,
                                           id_column='id',
                                           text_column='text',
                                           time_column='created_at')

    def fetch_app_android_data(self, url, config: Optional[SourceConfig] = None):
        config = self.get_source_config(self.config.android_config, config)
        source_config = PlayStoreScrapperConfig(
            app_url=url,
            lookup_period=config.lookup_period,
            max_count=config.limit_count
        )
        source_response_list = self.source_playstore.lookup(source_config)
        return self._create_obsei_response(source_response_list,
                                           id_column='reviewId',
                                           text_column='content',
                                           time_column='at')

    def fetch_app_ios_data(self, url, config: Optional[SourceConfig] = None):
        config = self.get_source_config(self.config.ios_config, config)
        source_config = AppStoreScrapperConfig(
            app_url=url,
            lookup_period=config.lookup_period,
            max_count=config.limit_count
        )
        source_response_list = self.source_appstore.lookup(source_config)
        return self._create_obsei_response(source_response_list,
                                           id_column='id',
                                           text_column='content',
                                           time_column='date')

    @staticmethod
    def _create_obsei_response(source_response_list: List, id_column: str, text_column: str, time_column: str):
        obsei_response_list = []

        for source_response in source_response_list:
            reference_id = str(source_response.meta[id_column])
            event_time = source_response.meta[time_column]

            # removing text to reduce DB size
            source_response.meta.pop(text_column, None)
            source_response.meta.pop(id_column, None)
            source_response.meta.pop(time_column, None)

            obsei_response_list.append(ObseiResponse(
                reference_id=reference_id,
                raw_text=source_response.processed_text,
                event_time=event_time,
                data=source_response.meta
            ))

        return obsei_response_list
