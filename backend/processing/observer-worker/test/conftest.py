import os
from unittest.mock import MagicMock

import boto3
import pytest
from moto import mock_sqs

from observer.domain.observer_job_handler import ObserverJobHandler
from observer.persistence.postgresql.raw_data_entity_manager import RawDataEntityManager
from observer.persistence.sqs.sqs_consumer import SqsConsumer
from observer.persistence.sqs.sqs_publisher import SqsPublisher


def side_effect_insert_raw_data(*args, **kwargs):
    return kwargs if "raw_data_list" not in kwargs else kwargs['raw_data_list']


# @pytest.fixture
# def pgmocker(transacted_postgresql_db):
#     with pgmock.mock(transacted_postgresql_db.connection) as mocker:
#         yield mocker


@pytest.fixture(scope='function')
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ['AWS_ACCESS_KEY_ID'] = 'testing'
    os.environ['AWS_SECRET_ACCESS_KEY'] = 'testing'
    os.environ['AWS_SECURITY_TOKEN'] = 'testing'
    os.environ['AWS_SESSION_TOKEN'] = 'testing'


@pytest.fixture(scope='function')
def sqs_client(aws_credentials):
    # setup
    with mock_sqs():
        yield boto3.client('sqs')
    # teardown


@pytest.fixture(scope='function')
def sqs_consumer(sqs_client):
    queue = sqs_client.create_queue(QueueName='consumer-queue')
    queue_url = queue['QueueUrl']
    yield SqsConsumer(queue_url=queue_url)


@pytest.fixture(scope='function')
def sqs_publisher(sqs_client):
    queue = sqs_client.create_queue(QueueName='publisher-queue')
    queue_url = queue['QueueUrl']
    yield SqsPublisher(queue_url=queue_url)


@pytest.fixture(scope='function')
def raw_data_entity_manager():
    # TODO: Not working fix this
    raw_data_entity_mgr = MagicMock(spec=RawDataEntityManager, side_effect=side_effect_insert_raw_data)
   # raw_data_entity_mgr.insert_raw_data = MagicMock(side_effect=side_effect_insert_raw_data)
    yield raw_data_entity_mgr


@pytest.fixture(scope='function')
def job_handler(sqs_publisher, raw_data_entity_manager):
    yield ObserverJobHandler(
        rawDataEntityManager=raw_data_entity_manager,
        sqsPublisher=sqs_publisher
    )


@pytest.fixture(scope='function')
def job_worker(sqs_consumer, job_handler):
    from observer.presentation.observer_job_controller import ObserverJobWorker

    yield ObserverJobWorker(
        consumer=sqs_consumer,
        job_handler=job_handler
    )
