from uuid import UUID

from prefect import flow

from service.common.utils import logger_utils
from service.workflow.nodes.event_rotator.event_rotator_db_provider import rotate_event_time_dp

logger = logger_utils.initialize_logger(__name__)


@flow
def event_time_rotator_workflow(tenant_id: UUID, period_days: int):
    try:
        rotate_event_time_dp(tenant_id, period_days)
    except Exception as error:
        logger.error("Unable to rotate event time")
        logger.exception(error)


event_time_rotator_wf = event_time_rotator_workflow
