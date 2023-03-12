import logging
from typing import Any, List

import boto3
# https://boto3.amazonaws.com/v1/documentation/api/latest/guide/sqs-example-sending-receiving-msgs.html
from obsei.misc.utils import obj_to_json
from pydantic import BaseModel, BaseSettings, Field, SecretStr

logger = logging.getLogger(__name__)


class RawDataEvent(BaseModel):
    tenant_id: str
    raw_data_id: int
    raw_text: str


class SqsPublisher(BaseSettings):
    region_name: str = Field('eu-west-1', env='AWS_REGION')
    aws_access_key_id: SecretStr = Field(SecretStr("dummy_key_id"), env='AWS_ACCESS_KEY_ID')
    aws_secret_access_key: SecretStr = Field(SecretStr("dummy_access_key"), env='AWS_SECRET_ACCESS_KEY')
    queue_url: str = Field('dummy_queue_url', env='AWS_SQS_ANALYSER_QUEUE')
    sqs: Any

    def __init__(self, **values: Any):
        super().__init__(**values)
        self.sqs = boto3.client(
            'sqs',
            region_name=self.region_name,
            use_ssl=False,
            aws_access_key_id=self.aws_access_key_id.get_secret_value(),
            aws_secret_access_key=self.aws_secret_access_key.get_secret_value()
        )

    def publish(self, messages: List[RawDataEvent]):
        message_ids = []
        for message in messages:
            message_body = obj_to_json(message).decode('UTF-8')
            logger.debug("Message: %s", message_body)
            response = self.sqs.send_message(
                QueueUrl=self.queue_url,
                DelaySeconds=1,
                MessageAttributes={},
                MessageBody=message_body
            )
            message_ids += response['MessageId']

        return message_ids
