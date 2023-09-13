import json
import logging
import sys
import time
from itertools import groupby
from typing import Optional, Any

from pydantic import BaseSettings, Field

from analyzer.model.api_request_response import AnalyzerJobRequest
from analyzer.model.data_store_request import DBStoreRequest
from analyzer.model.structure_data_request import UnstructuredDataRequest
from analyzer.persistence.db_entity_manager import DBEntityManager
from analyzer.persistence.sqs_consumer import SqsConsumer
from analyzer.service.text_analysis import review_analysis
from analyzer.worker.signal_handler import SignalHandler

root = logging.getLogger()
root.setLevel(logging.INFO)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
root.addHandler(handler)
logger = logging.getLogger(__name__)


class AnalyzerJobWorker(BaseSettings):
    worker_timelimit: int = Field(600, env='WORKER_TIMELIMIT_IN_SEC')
    max_empty_responses: int = Field(2, env='MAX_EMPTY_RESPONSES')

    consumer: Optional[SqsConsumer]
    structured_data_store: Optional[DBEntityManager]

    def __init__(self, **values: Any):
        super().__init__(**values)

        if not self.consumer:
            self.consumer = SqsConsumer()
        if not self.structured_data_store:
            self.structured_data_store = DBEntityManager()

    def run_worker_process(self):
        start_time = time.time()
        signal_handler = SignalHandler()
        exit_condition = False
        empty_responses = 0
        while not exit_condition and not signal_handler.received_signal:
            try:
                messages = self.consumer.receive_messages()
                if len(messages) == 0:
                    empty_responses += 1
                else:
                    processed_messages = []
                    empty_responses = 0
                    message_ids = ','.join([message.get('MessageId') for message in messages])
                    job_requests_by_id = {}

                    for message in messages:
                        try:
                            ajar = AnalyzerJobRequest.construct(**json.loads(message.get('Body')))
                            ajar.message = message
                            job_requests_by_id[ajar.raw_data_id] = ajar
                        except Exception as error:
                            logger.error("Unable to parse %s", message.get('MessageId'))
                            logger.exception(error)

                    job_requests_by_tenant = {
                        tenant_id: list(group)
                        for tenant_id, group in groupby(job_requests_by_id.values(), lambda ajr: ajr.tenant_id)
                    }

                    for tenant_id, job_requests in job_requests_by_tenant.items():
                        try:
                            data_requests = [UnstructuredDataRequest(
                                raw_data_id=job_request.raw_data_id,
                                raw_text=job_request.raw_text
                            ) for job_request in job_requests]

                            structured_data_list = review_analysis(tenant_id, data_requests)

                            for structured_data in structured_data_list:
                                structured_data_identifier = self.structured_data_store.insert_structured_data(
                                    data_request=DBStoreRequest(
                                        structured_data=structured_data,
                                        raw_data_identifier=structured_data.raw_data_id,
                                        tenant_id=tenant_id
                                    )
                                )
                                message = job_requests_by_id[structured_data.raw_data_id].message
                                processed_messages.append(message)
                                logger.info(
                                    "message_id=%s: structured_data_identifier=%d processed",
                                    message.get('MessageId'), structured_data_identifier
                                )
                        except Exception as error:
                            logger.error("Unable to process batch %s", message_ids)
                            logger.exception(error)
                            exit_condition = self.consumer.is_localstack()

                    if len(processed_messages) > 0:
                        self.consumer.delete_messages(processed_messages)

                elapsed_time = (time.time() - start_time)

                if elapsed_time >= self.worker_timelimit or empty_responses >= self.max_empty_responses:
                    logger.info("Exiting worker!! Elapsed Time = %f and Empty Responses = %d",
                                elapsed_time, empty_responses)
                    exit_condition = True

            except Exception as error:
                logger.exception("Unable to process message: %s", str(error))
                exit_condition = self.consumer.is_localstack()


if __name__ == '__main__':
    worker = AnalyzerJobWorker()
    worker.run_worker_process()
