import json
from datetime import timedelta, datetime
from unittest.mock import patch

import pytest

from config.context import MarketingCloudClientContext
from worker.client.marketing_cloud import MarketingCloudClient


@pytest.fixture
def mock_get():
    mock_call_patcher = patch('worker.client.marketing_cloud.requests.Session.send')
    mock_get = mock_call_patcher.start()

    yield mock_get

    mock_call_patcher.stop()


@pytest.fixture
def mock_auth_post():
    mock_call_patcher = patch('worker.client.marketing_cloud.requests.post')
    mock_get = mock_call_patcher.start()

    yield mock_get

    mock_call_patcher.stop()


@pytest.fixture
def test_context():
    return MarketingCloudClientContext(
        AUTH_ID="test",
        AUTH_URL="http://localhost",
        AUTH_SECRET_KEY="test",
        GET_PRODUCT_DATA_URL="http://localhost",
        SECRETS=dict(test="test_client_secret")
    )


@pytest.fixture
def expected_payload():
    todays_date = datetime.today()
    yesterdays_date = todays_date - timedelta(1)
    return {
        "Token": None,
        "Method": "getMarketingProductDetails",
        "startDate": yesterdays_date.strftime('%Y-%m-%d'),
        "endDate": todays_date.strftime('%Y-%m-%d')
    }


@pytest.fixture
def expected_header():
    return {
        'Content-Type': 'application/json'
    }


def json_wrapper(value):
    def json_func():
        return value
    return json_func


def test_marketing_cloud_fetch(mock_get, test_context, expected_payload, expected_header):
    # Given
    mock_get.return_value.status_code = 200
    mock_get.return_value.json = json_wrapper(dict(RequestID=42, Results="test"))
    client = MarketingCloudClient()
    expected = ("test", False)

    # When
    actual = client.fetch_product_data(test_context)

    # Then
    assert actual == expected
    assert client.request_id is None
    assert json.loads(mock_get.call_args[0][0].body) == expected_payload
    assert mock_get.call_args[0][0].headers['Content-Type'] == expected_header['Content-Type']


def test_marketing_cloud_fetch_multiple_calls(mock_get, test_context, expected_payload, expected_header):
    # Given
    mock_get.return_value.status_code = 200
    mock_get.return_value.json = json_wrapper(dict(RequestID=42, Results="test", HasMoreRows=True))
    client = MarketingCloudClient()
    expected1 = ("test", True)
    expected2 = ("test2", False)

    # When
    actual1 = client.fetch_product_data(test_context)
    mock_get.return_value.json = json_wrapper(dict(RequestID=43, Results="test2", HasMoreRows=False))
    expected_payload['RequestID'] = 42
    actual2 = client.fetch_product_data(test_context)

    # Then
    assert actual1 == expected1
    assert actual2 == expected2
    assert client.request_id is None
    assert json.loads(mock_get.call_args[0][0].body) == expected_payload
    assert mock_get.call_args[0][0].headers['Content-Type'] == expected_header['Content-Type']


def test_set_access_token(mock_auth_post, test_context):
    # Given
    mock_auth_post.return_value.status_code = 200
    mock_auth_post.return_value.content = json.dumps(dict(access_token="test"))
    mock_auth_post.return_value.json = json_wrapper(dict(access_token="test"))
    client = MarketingCloudClient()
    expected = "test"
    expected_body = {
        "grant_type": "client_credentials",
        "client_id": test_context.AUTH_ID,
        "client_secret": test_context.SECRETS.get(test_context.AUTH_SECRET_KEY)
    }

    # When
    client.set_access_token(test_context)

    # Then
    assert client.access_token == expected
    mock_auth_post.assert_called_once_with(test_context.AUTH_URL, data=expected_body)
