from uuid import UUID

from prefect import flow

from service.common.utils import logger_utils
from service.common.utils.dateutils import get_period_datetime
from service.common.utils.utils import split_array
from service.workflow.infra.workflow_db_provider import get_unprocessed_data_dp, insert_structured_data_dp
from service.workflow.nodes.analyzer.domain_models import UnstructuredDataRequest
from service.workflow.nodes.analyzer.text_analysis import review_analysis

logger = logger_utils.initialize_logger(__name__)


@flow
def analyzer_workflow(tenant_id: UUID, lookup_period: str, limit_count: int = 0):
    try:
        messages = get_unprocessed_data_dp(tenant_id, get_period_datetime(lookup_period), limit_count)
        message_ids = [message.identifier for message in messages]
        logger.info("Found %d unprocessed reviews", len(messages))

        try:
            data_requests = [UnstructuredDataRequest(
                raw_data_id=message.identifier,
                raw_text=message.raw_text
            ) for message in messages]

            for review_list in split_array(data_requests, 50):
                structured_data_list = review_analysis(tenant_id, review_list)

                for structured_data in structured_data_list:
                    structured_data_identifier = insert_structured_data_dp(tenant_id=tenant_id, structured_data=structured_data)
                    logger.info("structured_data_identifier=%d processed", structured_data_identifier)

        except Exception as error:
            logger.error("Analyzer: unable to process batch %s", message_ids)
            logger.exception(error)

    except Exception as error:
        logger.error("Unable to fetch batch")
        logger.exception(error)


analyzer_wf = analyzer_workflow
