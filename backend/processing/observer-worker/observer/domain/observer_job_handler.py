import logging
from typing import Dict, List, Optional, Any
from uuid import UUID

from pydantic import Field, BaseSettings

from observer.domain.raw_data import RawData
from observer.integration.executor import BaseObserverExecutor, TwitterExecutor, PlayStoreExecutor, AppleStoreExecutor, \
    GoogleMapsExecutor, FacebookExecutor, RedditExecutor, GoogleNewsExecutor, ObseiResponse, SourceConfig
from observer.persistence.postgresql.raw_data_entity_manager import RawDataEntityManager
from observer.persistence.sqs.sqs_publisher import SqsPublisher, \
    RawDataEvent
from observer.presentation.model.observer_job_event import ObserverJobEvent, ObserverType

logger = logging.getLogger(__name__)


class ObserverJobHandler(BaseSettings):
    observer_executors: Optional[Dict[ObserverType, BaseObserverExecutor]]
    rawDataEntityManager: Optional[RawDataEntityManager]
    sqsPublisher: Optional[SqsPublisher]
    min_raw_text_length: int = Field(20, env='MIN_TEXT_LENGTH')

    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.observer_executors:
            self.observer_executors = {
                ObserverType.Twitter: TwitterExecutor(),
                ObserverType.Android: PlayStoreExecutor(),
                ObserverType.iOS: AppleStoreExecutor(),
                ObserverType.GoogleMaps: GoogleMapsExecutor(),
                ObserverType.Facebook: FacebookExecutor(),
                ObserverType.Reddit: RedditExecutor(),
                ObserverType.GoogleNews: GoogleNewsExecutor(),
            }
        if not self.rawDataEntityManager:
            self.rawDataEntityManager = RawDataEntityManager()
        if not self.sqsPublisher:
            self.sqsPublisher = SqsPublisher()

    def fetch_data(self, event: ObserverJobEvent) -> List[ObseiResponse]:
        source_config: Optional[SourceConfig] = None
        if event.limit_count and event.lookup_period:
            source_config = SourceConfig(
                lookup_period=event.lookup_period,
                limit_count=event.limit_count
            )

        return self.observer_executors[event.observer_type].fetch_data(event, source_config)

    def handle_job(self, job: ObserverJobEvent):
        data_list = self.fetch_data(job)
        logger.info(f'{job.observer_identifier} fetch count: {len(data_list)}')

        raw_data_list = [
            RawData(
                observer_id=job.observer_identifier,
                reference_id=unstructured_data.reference_id,
                parent_reference_id=unstructured_data.parent_reference_id,
                raw_text=unstructured_data.raw_text,
                unstructured_data=unstructured_data.data or {},
                event_time=unstructured_data.event_time
            )
            for unstructured_data in data_list
        ]

        success_raw_data_list = self.rawDataEntityManager.insert_raw_data(job.tenant_id, raw_data_list)

        events = [self.get_raw_data_event(job.tenant_id, raw_data)
                  for raw_data in success_raw_data_list
                  if len(raw_data.raw_text) > self.min_raw_text_length]

        if events:
            self.sqsPublisher.publish(events)

        return len(success_raw_data_list)

    @staticmethod
    def get_raw_data_event(tenant_id: UUID, raw_data: RawData):

        return RawDataEvent(
            tenant_id=str(tenant_id),
            raw_data_id=raw_data.identifier,
            raw_text=raw_data.raw_text
        )
