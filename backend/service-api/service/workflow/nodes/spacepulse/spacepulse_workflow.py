import logging
from uuid import UUID

from prefect import flow
from requests.exceptions import ConnectionError

from service.common.dateutils import get_period_datetime
from service.common.db.node_meta_entity_manager import (
    WorkflowNodeMetaEntityManager,
    NodeMetaState,
)
from service.common.db.tenant_config_entity_manager import TenantConfigEntityManager
from service.workflow.nodes.spacepulse.spacepulse_client import (
    SpacePulsePostRequest,
    spacepulse_post, SpacePulseTenantInfo,
)

# --------- Logging configuration ------------------------
# stop prefect verbose logging
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger().setLevel(logging.INFO)
logger = logging.getLogger(__name__)
# --------- Logging configuration ------------------------

wf_node_em = WorkflowNodeMetaEntityManager()
tenant_config = TenantConfigEntityManager()


@flow
def spacepulse_workflow(tenant_id: UUID, lookup_period: str):
    try:
        tenant_info = tenant_config.get_tenant_config(tenant_id, 'spacepulse_tenant_info')
        if not tenant_info:
            raise ValueError('Empty Tenant Info')

        messages: list[SpacePulsePostRequest] = wf_node_em.get_unsent_processed_data(
            tenant_id, get_period_datetime(lookup_period)
        )
        logger.info("SpacePulse messages to be sent: %d", len(messages))

        for message in messages:
            try:
                spacepulse_post(tenant_info=SpacePulseTenantInfo(**tenant_info), review_data=message)
                wf_node_em.update_status(tenant_id, message.id, NodeMetaState.SENT)
                logger.info("SpacePulse sent request=%s", message.to_json())

            except ConnectionError as ce:
                logger.error("Connection error. Message: %s\n%s", message.to_json(), ce)
                wf_node_em.log_error(tenant_id, message.id, str(ce))

            except Exception as error:
                logger.error("Error: %s, unable to process message %s", type(error), message.to_json())
                logger.exception(error)
                wf_node_em.log_error(tenant_id, message.id, str(error))

    except Exception as error:
        logger.error("Unable to process batch:")
        logger.exception(error)


spacepulse_wf = spacepulse_workflow
