from operator import attrgetter
from typing import Dict, List, Optional, Any, cast
from uuid import UUID

from prefect import flow, task

from service.app.business.business_db_provider import insert_raw_data_dp
from service.app.data.data_models import RawData
from service.common.utils import logger_utils
from service.workflow.nodes.observer.executor.base_executor import BaseObserverExecutor, ObserverType, ObserverJobData, SourceConfig, SourceResponse
from service.workflow.nodes.observer.executor.obsei_executors import TwitterExecutor, PlayStoreExecutor, AppleStoreExecutor, GoogleMapsExecutor, \
    FacebookExecutor, RedditExecutor
from service.workflow.nodes.observer.executor.outscraper_executors import GoogleNewsOutscraperExecutor, GoogleSearchOutscraperExecutor
from service.workflow.nodes.observer.observer_db_provider import get_observer_tasks_dp

logger = logger_utils.initialize_logger(__name__)

observer_executors: Dict[ObserverType, BaseObserverExecutor] = {
    ObserverType.Twitter: TwitterExecutor(),
    ObserverType.Android: PlayStoreExecutor(),
    ObserverType.iOS: AppleStoreExecutor(),
    ObserverType.GoogleMaps: GoogleMapsExecutor(),
    ObserverType.Facebook: FacebookExecutor(),
    ObserverType.Reddit: RedditExecutor(),
    ObserverType.GoogleNews: GoogleNewsOutscraperExecutor(),
    ObserverType.GoogleSearch: GoogleSearchOutscraperExecutor()
}


def fetch_data(event: ObserverJobData) -> List[SourceResponse]:
    source_config: Optional[SourceConfig] = None
    if event.limit_count and event.lookup_period:
        source_config = SourceConfig(
            lookup_period=event.lookup_period,
            limit_count=event.limit_count
        )

    return observer_executors[event.observer_type].fetch_data(event, source_config)


@task
def handle_job(job: ObserverJobData):
    data_list = fetch_data(job)
    if not data_list:
        return 0

    data_list.sort(key=attrgetter('event_time'))
    logger.info(f'{job.observer_id} fetch count: {data_list}')

    raw_data_list = [
        RawData(
            observer_id=job.observer_id,
            reference_id=unstructured_data.reference_id,
            parent_reference_id=unstructured_data.parent_reference_id,
            raw_text=unstructured_data.raw_text,
            unstructured_data=unstructured_data.data or {},
            event_time=unstructured_data.event_time
        )
        for unstructured_data in data_list
    ]

    success_raw_data_list = insert_raw_data_dp(job.tenant_id, raw_data_list)
    return len(success_raw_data_list)


@task
def get_observer_tasks(tenant_id: UUID):
    return get_observer_tasks_dp(tenant_id)


limit_count_map = {
    ObserverType.Twitter: 100,
    ObserverType.Android: 20,
    ObserverType.iOS: 100,
    ObserverType.GoogleMaps: 100,
    ObserverType.GoogleNews: 1,
    ObserverType.GoogleSearch: 1
}


def get_observer_limit(limit_count: int, observer_type: ObserverType):
    if limit_count > 0:
        return limit_count
    else:
        return limit_count_map.get(observer_type) or 20


@flow()
def observer_workflow(tenant_id: UUID, lookup_period: str, limit_count: int = 0):
    results: List[Dict[str, Any]] = get_observer_tasks(tenant_id) or cast(List[Dict[str, Any]], [])
    messages = [
        ObserverJobData(
            tenant_id=tenant_id,
            observer_id=result['identifier'],
            observer_type=result['type'],
            url=result['url'],
            query=result['query'],
            country=result['country'],
            language=result['language'],
            number_of_pages=result['number_of_pages'],
            page_id=result['page_id'],
            subreddit=result['subreddit'],
            limit_count=get_observer_limit(limit_count, result['type']),
            tbs=result['tbs']
        )
        for result in results
    ]

    for message in messages:
        try:
            message.lookup_period = lookup_period
            count = handle_job(message)
            logger.info("Handled observer jobs:%d", count)
        except Exception as error:
            logger.error("Unable to process observer:%s", message.observer_id)
            logger.error(error)


observer_wf = observer_workflow
