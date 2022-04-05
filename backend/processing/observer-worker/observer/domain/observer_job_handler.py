import logging
import os
from typing import Any, Dict

from observer.domain.raw_data import RawData
from observer.integration.obsei_client import ObseiClient, ObseiClientConfig, SourceConfig
from observer.persistence.postgresql.raw_data_entity_manager import RawDataEntityManager
from observer.persistence.sqs.sqs_publisher import SqsPublisher, \
    ObserverMessage, RawDataEvent, TextDataMessage, EntityMessage
from observer.presentation.model.observer_job_event import ObserverJobEvent, ObserverType
from observer.utils.dateutils import datetime_to_iso_format

logger = logging.getLogger(__name__)


class ObserverJobHandler:
    data_fetcher: Dict[ObserverType, Any]
    obsei_client: ObseiClient
    rawDataEntityManager: RawDataEntityManager
    sqsPublisher: SqsPublisher
    min_raw_text_length: int

    def __init__(self):
        self.data_fetcher = {
            ObserverType.twitter: self.fetch_twitter_data,
            ObserverType.android: self.fetch_android_data,
            ObserverType.ios: self.fetch_ios_data,
        }
        self.obsei_client = ObseiClient(ObseiClientConfig(
            twitter_config=SourceConfig(lookup_period='5m', limit_count=100),
            android_config=SourceConfig(lookup_period='5m', limit_count=10),
            ios_config=SourceConfig(lookup_period='5m', limit_count=450)
        ))
        self.rawDataEntityManager = RawDataEntityManager()
        self.sqsPublisher = SqsPublisher()
        self.min_raw_text_length = int(os.environ.get('MIN_TEXT_LENGTH', 20))

    def get_config_for_observer(self, observer_id):
        pass

    def handle_job(self, job: ObserverJobEvent):
        data_list = self.data_fetcher[job.observer_type](job)
        logger.info(
            f'{job.observer_identifier}:{job.observer_name}:{job.observer_type.name} fetch count: {len(data_list)}')

        raw_data_list = [
            RawData(
                company_id=job.company_id,
                observer_id=job.observer_identifier,
                observer_name=job.observer_name,
                observer_type=job.observer_type,
                entity_id=job.entity_identifier,
                entity_name=job.entity_simple_name,
                regulated_entity_type=job.regulated_entity_type,
                reference_id=data.reference_id,
                parent_reference_id=data.parent_reference_id,
                raw_text=data.raw_text,
                data=data.data or {},
                event_time=data.event_time
            )
            for data in data_list
        ]

        success_raw_data_list = self.rawDataEntityManager.insert_raw_data(raw_data_list)

        events = [self.get_raw_data_event(job, raw_data)
                  for raw_data in success_raw_data_list
                  if len(raw_data.raw_text) > self.min_raw_text_length]

        if events:
            self.sqsPublisher.publish(events)

        return len(success_raw_data_list)

    @staticmethod
    def get_source_config(job_data, default_source_config: SourceConfig):
        if job_data.lookup_period or job_data.limit_count:
            lookup_period = job_data.lookup_period
            limit_count = job_data.limit_count
            return SourceConfig(
                lookup_period=lookup_period if lookup_period else default_source_config.lookup_period,
                limit_count=limit_count if limit_count else default_source_config.limit_count
            )
        else:
            return None

    def fetch_twitter_data(self, job_data: ObserverJobEvent):
        source_config = self.get_source_config(job_data, self.obsei_client.config.twitter_config)
        return self.obsei_client.fetch_twitter_data(job_data.twitter_handle, source_config)

    def fetch_android_data(self, job_data: ObserverJobEvent):
        source_config = self.get_source_config(job_data, self.obsei_client.config.android_config)
        return self.obsei_client.fetch_app_android_data(job_data.app_url, source_config)

    def fetch_ios_data(self, job_data: ObserverJobEvent):
        source_config = self.get_source_config(job_data, self.obsei_client.config.ios_config)
        return self.obsei_client.fetch_app_ios_data(job_data.app_url, source_config)

    @staticmethod
    def get_raw_data_event(job_data: ObserverJobEvent, raw_data: RawData):

        entity_message = EntityMessage(
            identifier=job_data.entity_identifier,
            simple_name=job_data.entity_simple_name,
            country=job_data.entity_country,
            city=job_data.entity_city)

        observer_message = ObserverMessage(
            identifier=job_data.observer_identifier,
            name=job_data.observer_name,
            type=job_data.observer_type.value,
            regulated_entity_type=job_data.regulated_entity_type)

        text_data_message = TextDataMessage(
            identifier=raw_data.identifier,
            raw_text=raw_data.raw_text,
            event_time=datetime_to_iso_format(raw_data.event_time))

        return RawDataEvent(
            company_id=raw_data.company_id,
            observer=observer_message,
            entity=entity_message,
            text_data=text_data_message
        )
