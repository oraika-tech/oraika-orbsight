import json
import logging
import time
from typing import Optional, Any

from pydantic import BaseSettings, Field

from observer.domain.observer_job_handler import ObserverJobHandler
from observer.persistence.sqs.sqs_consumer import SqsConsumer
from observer.presentation.model.observer_job_event import ObserverJobEvent
from observer.utils.signal_handler import SignalHandler

logger = logging.getLogger(__name__)


class ObserverJobWorker(BaseSettings):
    worker_timelimit: int = Field(600, env='WORKER_TIMELIMIT_IN_SEC')
    max_empty_responses: int = Field(2, env='MAX_EMPTY_RESPONSES')

    consumer: Optional[SqsConsumer]
    job_handler: Optional[ObserverJobHandler]

    def __init__(self, **values: Any):
        super().__init__(**values)

        if not self.consumer:
            self.consumer = SqsConsumer()
        if not self.job_handler:
            self.job_handler = ObserverJobHandler()

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
                        observer_job_event = ObserverJobEvent.construct(**json.loads(message.get('Body')))
                        count = self.job_handler.handle_job(observer_job_event)
                        logger.info("message_id=%s: Total %d events observed", message.get('MessageId'), count)
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
    worker = ObserverJobWorker()
    worker.run_worker_process()
