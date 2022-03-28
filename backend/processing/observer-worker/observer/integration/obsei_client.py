from typing import Optional, Dict, Any

from obsei.source import TwitterSourceConfig, TwitterSource, TwitterCredentials
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
            query=f'@{query}',
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

        return [
            ObseiResponse(
                reference_id=str(source_response.meta['id']),
                raw_text=source_response.processed_text,
                data=source_response.meta
            )
            for source_response in source_response_list
        ]

    def fetch_app_android_data(self, url, config: Optional[SourceConfig] = None):
        config = self.get_source_config(self.config.android_config, config)
        source_config = PlayStoreScrapperConfig(
            app_url=url,
            lookup_period=config.lookup_period,
            max_count=config.limit_count
        )

        source_response_list = self.source_playstore.lookup(source_config)

        return [
            ObseiResponse(
                reference_id=source_response.meta['reviewId'],
                raw_text=source_response.processed_text,
                data=source_response.meta
            )
            for source_response in source_response_list
        ]

    def fetch_app_ios_data(self, url, config: Optional[SourceConfig] = None):
        config = self.get_source_config(self.config.android_config, config)
        source_config = AppStoreScrapperConfig(
            app_url=url,
            lookup_period=config.lookup_period,
            max_count=config.limit_count
        )

        source_response_list = self.source_appstore.lookup(source_config)

        return [
            ObseiResponse(
                reference_id=str(source_response.meta['id']),
                raw_text=source_response.processed_text,
                data=source_response.meta
            )
            for source_response in source_response_list
        ]
