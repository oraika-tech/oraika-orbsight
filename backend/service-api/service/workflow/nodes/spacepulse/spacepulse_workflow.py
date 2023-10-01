from uuid import UUID

from prefect import flow
from requests.exceptions import ConnectionError

from service.common.models import NodeMetaState
from service.common.utils import logger_utils
from service.common.utils.dateutils import get_period_datetime
from service.workflow.infra.workflow_db_provider import get_unsent_processed_data_dp, update_status_dp, log_wf_error_dp
from service.workflow.nodes.spacepulse.spacepulse_client import SpacePulsePostRequest, spacepulse_post
from service.workflow.nodes.spacepulse.spacepulse_db_provider import get_space_pulse_tenant_info

logger = logger_utils.initialize_logger(__name__)


@flow
def spacepulse_workflow(tenant_id: UUID, lookup_period: str):
    try:
        tenant_info = get_space_pulse_tenant_info(tenant_id, 'spacepulse_tenant_info')
        if not tenant_info:
            raise ValueError('Empty Tenant Info')

        messages: list[SpacePulsePostRequest] = get_unsent_processed_data_dp(
            tenant_id, get_period_datetime(lookup_period)
        )
        logger.info("SpacePulse messages to be sent: %d", len(messages))

        for message in messages:
            try:
                spacepulse_post(tenant_info=tenant_info, review_data=message)
                update_status_dp(tenant_id, message.id, NodeMetaState.SENT)
                logger.info("SpacePulse sent request=%s", message.to_json())

            except ConnectionError as ce:
                logger.error("Connection error. Message: %s\n%s", message.to_json(), ce)
                log_wf_error_dp(tenant_id, message.id, str(ce))

            except Exception as error:
                logger.error("Error: %s, unable to process message %s", type(error), message.to_json())
                logger.exception(error)
                log_wf_error_dp(tenant_id, message.id, str(error))

    except Exception as error:
        logger.error("Unable to process batch:")
        logger.exception(error)


spacepulse_wf = spacepulse_workflow
