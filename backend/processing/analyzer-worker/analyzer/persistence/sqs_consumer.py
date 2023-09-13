import logging
from typing import Any

import boto3
from botocore.exceptions import ClientError
from pydantic import BaseSettings, Field, SecretStr

logger = logging.getLogger(__name__)


class SqsConsumer(BaseSettings):
    region_name: str = Field('eu-west-1', env='AWS_REGION')
    aws_access_key_id: SecretStr = Field(SecretStr('dummy_key_id'), env='AWS_ACCESS_KEY_ID')
    aws_secret_access_key: SecretStr = Field(SecretStr('dummy_access_key'), env='AWS_SECRET_ACCESS_KEY')
    # Set env for localstack: 'http://queue.localhost.localstack.cloud:4566/000000000000/sample-queue'
    queue_url: str = Field('dummy_queue_url', env='AWS_SQS_ANALYZER_QUEUE')
    max_messages: int = Field(10, env='MAX_POLL_MESSAGES')
    wait_time: int = Field(5, env='MAX_WAIT_TIME_IN_SEC')
    sqs: Any

    def __init__(self, **values: Any):
        super().__init__(**values)
        endpoint_url = 'http://localhost:4566' if self.is_localstack() else None
        self.sqs = boto3.client(
            'sqs',
            region_name=self.region_name,
            use_ssl=False,
            endpoint_url=endpoint_url,
            aws_access_key_id=self.aws_access_key_id.get_secret_value(),
            aws_secret_access_key=self.aws_secret_access_key.get_secret_value()
        )

    def is_localstack(self):
        return 'localhost' in self.queue_url

    def receive_messages(self):
        try:
            messages = self.sqs.receive_message(
                QueueUrl=self.queue_url,
                MessageAttributeNames=['All'],
                MaxNumberOfMessages=self.max_messages,
                WaitTimeSeconds=self.wait_time
            )
        except ClientError as error:
            logger.exception("Couldn't receive messages from queue: %s", self.queue_url)
            raise error
        else:
            return messages.get('Messages', [])

    def delete_messages(self, messages):
        try:
            entries = [{
                'Id': str(ind),
                'ReceiptHandle': msg.get('ReceiptHandle')
            } for ind, msg in enumerate(messages)]
            response = self.sqs.delete_message_batch(
                QueueUrl=self.queue_url,
                Entries=entries
            )
            if 'Successful' in response:
                for msg_meta in response['Successful']:
                    logger.info("Deleted %s", messages[int(msg_meta['Id'])].get('ReceiptHandle'))
            if 'Failed' in response:
                for msg_meta in response['Failed']:
                    logger.warning(
                        "Could not delete %s",
                        messages[int(msg_meta['Id'])].get('ReceiptHandle')
                    )
        except ClientError:
            logger.exception("Couldn't delete messages from queue %s", self.queue_url)
        else:
            return response
