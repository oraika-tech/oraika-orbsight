from uuid import UUID

from prefect import flow

from service.common.utils import logger_utils
from service.common.utils.dateutils import get_period_datetime
from service.workflow.infra.workflow_db_provider import get_unprocessed_data_dp, insert_structured_data_dp
from service.workflow.nodes.analyzer.domain_models import UnstructuredDataRequest
from service.workflow.nodes.analyzer.text_analysis import review_analysis

logger = logger_utils.initialize_logger(__name__)


@flow
def analyzer_workflow(tenant_id: UUID, lookup_period: str):
    try:
        messages = get_unprocessed_data_dp(tenant_id, get_period_datetime(lookup_period))
        message_ids = [message.identifier for message in messages]
        logger.info("Found %d unprocessed reviews", len(messages))

        try:
            data_requests = [UnstructuredDataRequest(
                raw_data_id=message.identifier,
                raw_text=message.raw_text
            ) for message in messages]

            structured_data_list = review_analysis(tenant_id, data_requests)

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
