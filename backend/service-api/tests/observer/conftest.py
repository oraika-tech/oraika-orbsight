import os
from unittest.mock import MagicMock

import boto3
import pytest
from moto import mock_sqs

from service.common.db.raw_data_entity_manager import RawDataEntityManager


def side_effect_insert_raw_data(*args, **kwargs):
    return kwargs if "raw_data_list" not in kwargs else kwargs['raw_data_list']


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
def raw_data_entity_manager():
    # TODO: Not working fix this
    raw_data_entity_mgr = MagicMock(spec=RawDataEntityManager, side_effect=side_effect_insert_raw_data)
    # raw_data_entity_mgr.insert_raw_data = MagicMock(side_effect=side_effect_insert_raw_data)
    yield raw_data_entity_mgr
