import logging
import sys
from uuid import UUID

from prefect import flow

from service.common.db.processed_data_entity_manager import ProcessedDataEntityManager
from service.common.db.raw_data_entity_manager import RawDataEntityManager

# todo: move all logger to a function and call that from each workflow
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
def event_time_rotator_workflow(tenant_id: UUID, period_days: int):
    try:
        raw_data_entity_manager.rotate_event_time(tenant_id, period_days)
    except Exception as error:
        logger.error("Unable to rotate event time")
        logger.exception(error)


event_time_rotator_wf = event_time_rotator_workflow
