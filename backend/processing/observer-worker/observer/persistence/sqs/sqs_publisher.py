import json
import logging
from typing import Any, List, Optional

import boto3
# https://boto3.amazonaws.com/v1/documentation/api/latest/guide/sqs-example-sending-receiving-msgs.html
from obsei.misc.utils import obj_to_json
from pydantic import BaseSettings, SecretStr, Field, BaseModel

logger = logging.getLogger(__name__)


class ObserverMessage(BaseModel):
    identifier: int
    name: str
    type: int


class EntityMessage(BaseModel):
    identifier: int
    simple_name: str
    type: str
    country: Optional[str]
    city: Optional[str]


class TextDataMessage(BaseModel):
    identifier: int
    raw_text: str


class RawDataEvent(BaseModel):
    company_id: int
    observer: ObserverMessage
    entity: EntityMessage
    text_data: TextDataMessage


class SqsPublisher(BaseSettings):
    region_name: str = Field('eu-west-1', env='AWS_REGION')
    aws_access_key_id: SecretStr = Field(None, env='AWS_ACCESS_KEY_ID')
    aws_secret_access_key: SecretStr = Field(None, env='AWS_SECRET_ACCESS_KEY')
    queue_url: str = Field(None, env='AWS_SQS_ANALYSER_QUEUE')
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
