from unittest.mock import patch

import pytest

from pathlib import Path
from service.api.v1.marketing_cloud import ProductData


@pytest.fixture(scope="function")
def mock_secrets():
    mock_call_patcher = patch('util.secrets.get_secrets')
    mock_call = mock_call_patcher.start()

    yield mock_call

    mock_call_patcher.stop()


@pytest.fixture
def test_env():
    import os
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


@pytest.fixture
def teardown():
    import os
    os.environ['WORK_QUEUE_PATH'] = './test_queue/api_test'
    yield
    import shutil
    shutil.rmtree('./test_queue/api_test')
    del os.environ['WORK_QUEUE_PATH']


def test_product_data_class(mock_secrets, teardown):
    # Given
    mock_secrets.return_value = dict()
    expected_result = ({"data": {"message": "ok"}}, 201)

    # When
    import os
    print(os.getenv('WORK_QUEUE_PATH'))
    actual = ProductData.post()

    # Then
    assert actual == expected_result


def test_product_data_class_second_attempt_fails(mock_secrets, teardown):
    # Given
    mock_secrets.return_value = dict()
    expected_result = ({"error": {"message": "unlocked item already exists"}}, 409)

    # When
    ProductData.post()
    actual = ProductData.post()

    # Then
    assert actual == expected_result


def test_product_data_class_attempt_on_locked_item_fails(mock_secrets, teardown):
    # Given
    mock_secrets.return_value = dict()
    expected_result = ({"error": {"message": "locked item already exists"}}, 409)

    # When
    Path('./test_queue/api_test').mkdir(exist_ok=True)
    Path('./test_queue/api_test/product-data.lock').touch()
    actual = ProductData.post()

    # Then
    assert actual == expected_result
