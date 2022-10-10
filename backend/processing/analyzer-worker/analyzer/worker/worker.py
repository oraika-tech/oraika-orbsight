import json
import logging
import sys
import time
from typing import Optional, Any

from pydantic import BaseSettings, Field

from analyzer.persistence.sqs_consumer import SqsConsumer
from analyzer.worker.signal_handler import SignalHandler
from analyzer.worker.tiyaro_exception import TiyaroException
from analyzer.model.api_request_response import AnalyzerJobRequest
from analyzer.model.data_store_request import DBStoreRequest
from analyzer.model.structure_data_request import UnstructuredDataRequest
from analyzer.persistence.db_entity_manager import DBEntityManager
from analyzer.service.structure_data_extractor import StructuredDataExtractor

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
    structure_data_extractor: Optional[StructuredDataExtractor]
    structured_data_store: Optional[DBEntityManager]

    def __init__(self, **values: Any):
        super().__init__(**values)

        if not self.consumer:
            self.consumer = SqsConsumer()
        if not self.structure_data_extractor:
            self.structure_data_extractor = StructuredDataExtractor()
        if not self.structured_data_store:
            self.structured_data_store = DBEntityManager()

    def run_worker_process(self):
        start_time = time.time()
        signal_handler = SignalHandler()
        exit_condition = False
        empty_responses = 0
        while not exit_condition and not signal_handler.received_signal:
            messages = self.consumer.receive_messages()
            if len(messages) == 0:
                empty_responses += 1
            else:
                processed_messages = []
                empty_responses = 0
                for message in messages:
                    try:
                        job_request = AnalyzerJobRequest.construct(**json.loads(message.get('Body')))
                        structured_data = self.structure_data_extractor.extract_structure(
                            UnstructuredDataRequest(
                                tenant_id=job_request.tenant_id,
                                raw_text=job_request.raw_text
                            )
                        )
                        structured_data_identifier = self.structured_data_store.insert_structured_data(
                            data_request=DBStoreRequest(
                                structured_data=structured_data,
                                raw_data_identifier=job_request.raw_data_id,
                                tenant_id=job_request.tenant_id
                            )
                        )
                        logger.info(
                            "message_id=%s: structured_data_identifier=%d processed",
                            message.get('MessageId'), structured_data_identifier
                        )
                    except TiyaroException as ex:
                        logger.error(f"Tiyaro Exception occur: {ex}")
                    except Exception as error:
                        logger.error("Unable to process %s", message.get('MessageId'))
                        logger.error(error)
                    else:
                        processed_messages.append(message)

                if len(processed_messages) > 0:
                    self.consumer.delete_messages(processed_messages)

            elapsed_time = (time.time() - start_time)

            if elapsed_time >= self.worker_timelimit or empty_responses >= self.max_empty_responses:
                logger.info("Exiting worker!! Elapsed Time = %f and Empty Responses = %d", elapsed_time,
                            empty_responses)
                exit_condition = True


if __name__ == '__main__':
    worker = AnalyzerJobWorker()
    worker.run_worker_process()
