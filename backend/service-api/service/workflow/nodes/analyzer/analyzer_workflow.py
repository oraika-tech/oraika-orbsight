import logging
import sys
from uuid import UUID

from prefect import flow

from service.common.dateutils import get_period_datetime
from service.common.db.processed_data_entity_manager import ProcessedDataEntityManager, DBStoreRequest
from service.common.db.raw_data_entity_manager import RawDataEntityManager
from service.workflow.nodes.analyzer.domain_models import UnstructuredDataRequest
from service.workflow.nodes.analyzer.text_analysis import review_analysis

root = logging.getLogger()
root.setLevel(logging.INFO)
logging.getLogger("httpx").setLevel(logging.WARNING)  # stop prefect verbose logging

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(filename)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
root.addHandler(handler)
logger = logging.getLogger(__name__)

structured_data_store = ProcessedDataEntityManager()
raw_data_entity_manager = RawDataEntityManager()


@flow
def analyzer_workflow(tenant_id: UUID, lookup_period: str):
    try:
        messages = raw_data_entity_manager.get_unprocessed_data(tenant_id, get_period_datetime(lookup_period))
        message_ids = [message.identifier for message in messages]
        logger.info("Found %d unprocessed reviews", len(messages))

        try:
            data_requests = [UnstructuredDataRequest(
                raw_data_id=message.identifier,
                raw_text=message.raw_text
            ) for message in messages]

            structured_data_list = review_analysis(tenant_id, data_requests)

            for structured_data in structured_data_list:
                structured_data_identifier = structured_data_store.insert_structured_data(
                    data_request=DBStoreRequest(
                        structured_data=structured_data,
                        raw_data_identifier=structured_data.raw_data_id,
                        tenant_id=tenant_id
                    )
                )
                logger.info("structured_data_identifier=%d processed", structured_data_identifier)

        except Exception as error:
            logger.error("Analyzer: unable to process batch %s", message_ids)
            logger.exception(error)

    except Exception as error:
        logger.error("Unable to fetch batch")
        logger.exception(error)


analyzer_wf = analyzer_workflow
