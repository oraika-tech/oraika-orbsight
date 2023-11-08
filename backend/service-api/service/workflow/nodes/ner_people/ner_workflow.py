from uuid import UUID

from prefect import flow

from service.common.utils import logger_utils
from service.common.utils.dateutils import get_period_datetime
from service.workflow.nodes.analyzer.domain_models import UnstructuredDataRequest
from service.workflow.nodes.analyzer.text_analysis import text_people_analysis
from service.workflow.nodes.ner_people.ner_db_provider import add_people_data, get_unprocessed_ner_data

logger = logger_utils.initialize_logger(__name__)


@flow
def ner_workflow(tenant_id: UUID, lookup_period: str, limit_count: int = 0):
    try:
        messages = get_unprocessed_ner_data(tenant_id, get_period_datetime(lookup_period), limit_count)
        message_ids = [message.identifier for message in messages]
        logger.info("Found %d unprocessed reviews", len(messages))

        try:
            data_requests = [UnstructuredDataRequest(
                raw_data_id=message.identifier,
                raw_text=message.raw_text
            ) for message in messages]

            review_list = [el.dict() for el in data_requests]
            result_data_list = text_people_analysis(review_list)
            logger.info("Processed: %d Result: %s", len(result_data_list), result_data_list)
            add_people_data(tenant_id, result_data_list)

        except Exception as error:
            logger.error("Analyzer: unable to process batch %s", message_ids)
            logger.exception(error)

    except Exception as error:
        logger.error("Unable to fetch batch")
        logger.exception(error)


ner_wf = ner_workflow
