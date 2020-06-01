import os
from unittest.mock import patch

import pytest
from kasasa_common.context import DatabaseContext

from config.context import build_context, WorkQueueContext, WorkerContext, ServiceContext
from config import WORKER_SQL_PATH


@pytest.fixture(scope="function")
def mock_secrets():
    mock_call_patcher = patch('util.secrets.get_secrets')
    mock_call = mock_call_patcher.start()

    yield mock_call

    mock_call_patcher.stop()


@pytest.fixture
def test_env():
    test_env_vars = dict(
        DATABASE_HOST="DATABASE_HOST",
        DATABASE_PORT="5555",
        DATABASE_USERNAME="DATABASE_USERNAME",
        DATABASE_PASSWORD_KEY="DATABASE_PASSWORD_KEY"
    )
    os.environ.update(test_env_vars)

    yield test_env_vars

    for key in test_env_vars.keys():
        del os.environ[key]


def test_build_service_context(mock_secrets, test_env):
    # Given
    mock_secrets.return_value = dict()

    # When
    actual = build_context('service', **test_env)

    # Then
    assert isinstance(actual, ServiceContext)
    assert isinstance(actual.WORK_QUEUE_CONTEXT, WorkQueueContext)


def test_build_worker_context(mock_secrets, test_env):
    # Given
    mock_secrets.return_value = dict()

    # When
    actual = build_context('worker', **test_env)

    # Then
    assert isinstance(actual, WorkerContext)
    assert isinstance(actual.READER_CONTEXT, DatabaseContext)
    assert isinstance(actual.WRITER_CONTEXT, DatabaseContext)

    assert actual.SQL_PATH == WORKER_SQL_PATH

    assert actual.WORK_QUEUE_CONTEXT.PATH == './work_queue'
    assert actual.WORK_QUEUE_CONTEXT.TYPE == 'filesystem'

    assert actual.READER_CONTEXT.VAULT_SECRETS == dict()
    assert actual.READER_CONTEXT.DATABASE_HOST == "DATABASE_HOST"
    assert actual.READER_CONTEXT.DATABASE_PORT == 5555
    assert actual.READER_CONTEXT.DATABASE_USERNAME == "DATABASE_USERNAME"
    assert actual.READER_CONTEXT.DATABASE_PASSWORD_KEY == "DATABASE_PASSWORD_KEY"

    assert actual.WRITER_CONTEXT.VAULT_SECRETS == dict()
    assert actual.WRITER_CONTEXT.DATABASE_HOST == "DATABASE_HOST"
    assert actual.WRITER_CONTEXT.DATABASE_PORT == 5555
    assert actual.WRITER_CONTEXT.DATABASE_USERNAME == "DATABASE_USERNAME"
    assert actual.WRITER_CONTEXT.DATABASE_PASSWORD_KEY == "DATABASE_PASSWORD_KEY"

    assert actual.PRODUCER_CONSUMER_CONTEXT.QUEUE_KWARGS == dict(max_size=50)
    assert actual.PRODUCER_CONSUMER_CONTEXT.MAX_CONSUMERS == 5
    assert actual.PRODUCER_CONSUMER_CONTEXT.QUEUE_TYPE == 'memory'

    assert actual.SLEEP_TIME == 60
