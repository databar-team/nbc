
from unittest.mock import MagicMock

import pytest
from kasasa_common.queue import get_queue_interface

from config.context import MarketingCloudClientContext
from config.shared_text import QueueKeys
from worker.manager.producers import ProductDataProducer


@pytest.fixture
def test_context():
    return MarketingCloudClientContext(
        AUTH_ID="test",
        AUTH_URL="http://localhost",
        AUTH_SECRET_KEY="test",
        GET_PRODUCT_DATA_URL="http://localhost",
        SECRETS=dict(test="test_client_secret")
    )


def test_product_data_producer_func(test_context):
    # Given
    return_data = [dict(AccountNumber="99999", test_value="test")]
    producer = ProductDataProducer(test_context)
    producer.client.set_access_token = MagicMock()
    producer.client.fetch_product_data = MagicMock(side_effect=[(return_data, False)])
    test_queue = get_queue_interface('memory')()
    expected = dict(job_type=QueueKeys.PRODUCT_DATA, payload=dict(fi_id="99999", product_data=return_data))

    # When
    producer.producer_func(test_queue)
    actual = test_queue.get()

    # Then
    assert actual == expected


def test_product_data_producer_func_has_more(test_context):
    # Given
    return_data1 = [dict(AccountNumber="99999", test_value="test")]
    return_data2 = [dict(AccountNumber="5431", test_value="test2")]
    producer = ProductDataProducer(test_context)
    producer.client.set_access_token = MagicMock()
    producer.client.fetch_product_data = MagicMock(side_effect=[(return_data1, True), (return_data2, False)])
    test_queue = get_queue_interface('memory')()
    expected1 = dict(job_type=QueueKeys.PRODUCT_DATA, payload=dict(fi_id="99999", product_data=return_data1))
    expected2 = dict(job_type=QueueKeys.PRODUCT_DATA, payload=dict(fi_id="5431", product_data=return_data2))

    # When
    producer.producer_func(test_queue)
    actual1 = test_queue.get()
    actual2 = test_queue.get()

    # Then
    assert actual1 == expected1
    assert actual2 == expected2


def test_product_data_producer_func_one_return_multiple_fis(test_context):
    # Given
    return_data1 = [dict(AccountNumber="99999", test_value="test"), dict(AccountNumber="5431", test_value="test2")]
    producer = ProductDataProducer(test_context)
    producer.client.set_access_token = MagicMock()
    producer.client.fetch_product_data = MagicMock(side_effect=[(return_data1, False)])
    test_queue = get_queue_interface('memory')()
    expected1 = dict(job_type=QueueKeys.PRODUCT_DATA, payload=dict(fi_id="99999", product_data=[return_data1[0]]))
    expected2 = dict(job_type=QueueKeys.PRODUCT_DATA, payload=dict(fi_id="5431", product_data=[return_data1[1]]))

    # When
    producer.producer_func(test_queue)
    actual1 = test_queue.get()
    actual2 = test_queue.get()

    # Then
    assert actual1 == expected1
    assert actual2 == expected2


def test_product_data_producer_func_one_return_multiple_fis_multiple_results(test_context):
    # Given
    return_data1 = [
        dict(AccountNumber="99999", test_value="test"),
        dict(AccountNumber="5431", test_value="test2"),
        dict(AccountNumber="99999", test_value="test3"),
        dict(AccountNumber="5431", test_value="test4")
    ]
    producer = ProductDataProducer(test_context)
    producer.client.set_access_token = MagicMock()
    producer.client.fetch_product_data = MagicMock(side_effect=[(return_data1, False)])
    test_queue = get_queue_interface('memory')()
    expected1 = dict(job_type=QueueKeys.PRODUCT_DATA, payload=dict(fi_id="99999", product_data=[
        return_data1[0], return_data1[2]
    ]))
    expected2 = dict(job_type=QueueKeys.PRODUCT_DATA, payload=dict(fi_id="5431", product_data=[
        return_data1[1], return_data1[3]
    ]))

    # When
    producer.producer_func(test_queue)
    actual1 = test_queue.get()
    actual2 = test_queue.get()

    # Then
    assert actual1 == expected1
    assert actual2 == expected2

