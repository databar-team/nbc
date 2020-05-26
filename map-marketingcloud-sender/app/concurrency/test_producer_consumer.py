import os
import pytest
import requests

from config.context import set_context, get_context
from concurrency.producer_consumer import ProducerConsumer
from tests.mock.marketing_cloud import MockMarketingCloudClient, MockResponse
from client.marketing_cloud import RETRY_LIMIT


@pytest.fixture(scope="function")
def context():
    set_context()

    return get_context()


@pytest.fixture(scope="function")
def one_valid_fi_ids():
    return [2211]


@pytest.fixture(scope="function")
def many_valid_fi_ids():
    return [2211, 99999]


@pytest.fixture()
def mocked_client_200():
    client = MockMarketingCloudClient()

    response = MockResponse()
    response.status_code = 200

    client.add_mocked_response(response)
    return client


@pytest.fixture()
def mocked_client_401():
    client = MockMarketingCloudClient()

    response1 = MockResponse()
    response1.status_code = 401

    response2 = MockResponse()
    response2.status_code = 200

    client.add_mocked_response(response1)
    client.add_mocked_response(response2)

    return client


@pytest.fixture()
def mocked_client_401_multiple():
    client = MockMarketingCloudClient()

    response = MockResponse()
    response.status_code = 401

    client.add_mocked_response(response)
    client.add_mocked_response(response)
    client.add_mocked_response(response)
    client.add_mocked_response(response)

    return client


def test_producer_consumer(context, mocked_client_200, one_valid_fi_ids):
    # given
    the_work = None

    def producer_test_func(context, queue, fi_id):
        nonlocal the_work
        the_work = "{}_producer".format(fi_id)

        queue.put({
            "fi_id": fi_id,
            "data": the_work
        })

    def consumer_test_func(context, client, msg):
        data = msg["data"]
        fi_id = msg["fi_id"]

        data += "_consumer"

        client.send(context, fi_id, data)

    cp = ProducerConsumer(context, mocked_client_200, one_valid_fi_ids)
    cp.add_producer("test_producer", producer_test_func)
    cp.set_consumer_func(consumer_test_func)
    cp.set_num_consumers(1)

    # when
    cp.run()

    # then
    assert "2211_producer" == the_work
    assert 1 == len(mocked_client_200.datas)
    assert 1 == len(mocked_client_200.fi_ids)
    assert "2211_producer_consumer" == mocked_client_200.datas[0]
    assert 2211 == mocked_client_200.fi_ids[0]


def test_producer_consumer_multiples(context, mocked_client_200, one_valid_fi_ids):
    # given
    def producer_1_test_func(context, queue, fi_id):
        queue.put({
            "fi_id": fi_id,
            "data": "from_producer_1"
        })

    def producer_2_test_func(context, queue, fi_id):
        queue.put({
            "fi_id": fi_id,
            "data": "from_producer_2"
        })

    def consumer_test_func(context, client, msg):
        data = msg["data"]
        fi_id = msg["fi_id"]

        data += "_consumer"

        client.send(context, fi_id, data)

    cp = ProducerConsumer(context, mocked_client_200, one_valid_fi_ids)
    cp.add_producer("producer_1", producer_1_test_func)
    cp.add_producer("producer_2", producer_2_test_func)
    cp.set_consumer_func(consumer_test_func)
    cp.set_num_consumers(2)

    # when
    cp.run()

    # then
    assert 2 == len(mocked_client_200.datas)
    assert 1 == len(mocked_client_200.fi_ids)
    assert "from_producer_1_consumer" in mocked_client_200.datas
    assert "from_producer_2_consumer" in mocked_client_200.datas
    assert 2211 == mocked_client_200.fi_ids[0]


def test_producer_consumer_multiples_and_fi_ids(context, mocked_client_200, many_valid_fi_ids):
    # given
    def producer_1_test_func(context, queue, fi_id):
        queue.put({
            "fi_id": fi_id,
            "data": "{}_from_producer_1".format(fi_id)
        })

    def producer_2_test_func(context, queue, fi_id):
        queue.put({
            "fi_id": fi_id,
            "data": "{}_from_producer_2".format(fi_id)
        })

    def consumer_test_func(context, client, msg):
        data = msg["data"]
        fi_id = msg["fi_id"]

        data += "_consumer"

        client.send(context, fi_id, data)

    cp = ProducerConsumer(context, mocked_client_200, many_valid_fi_ids)
    cp.add_producer("producer_1", producer_1_test_func)
    cp.add_producer("producer_2", producer_2_test_func)
    cp.set_consumer_func(consumer_test_func)
    cp.set_num_consumers(2)

    # when
    cp.run()

    # then
    assert 4 == len(mocked_client_200.datas)
    assert 2 == len(mocked_client_200.fi_ids)
    assert "2211_from_producer_1_consumer" in mocked_client_200.datas
    assert "2211_from_producer_2_consumer" in mocked_client_200.datas
    assert "99999_from_producer_1_consumer" in mocked_client_200.datas
    assert "99999_from_producer_2_consumer" in mocked_client_200.datas
    assert 2211 in mocked_client_200.fi_ids
    assert 99999 in mocked_client_200.fi_ids


def test_producer_consumer_invalid_access_token_max_retry(context, mocked_client_401_multiple, one_valid_fi_ids):
    # given
    result = None

    def producer_test_func(context, queue, fi_id):
        queue.put({
            "fi_id": fi_id,
            "data": "filler"
        })

    def consumer_test_func(context, client, msg):
        nonlocal result

        data = msg["data"]
        fi_id = msg["fi_id"]

        result = client.send(context, fi_id, data)

    cp = ProducerConsumer(context, mocked_client_401_multiple, one_valid_fi_ids)
    cp.add_producer("producer", producer_test_func)
    cp.set_consumer_func(consumer_test_func)
    cp.set_num_consumers(1)

    # when
    cp.run()

    # then
    assert RETRY_LIMIT + 1 == len(mocked_client_401_multiple.datas)
    assert False == result


def test_producer_consumer_invalid_access_token(context, mocked_client_401, one_valid_fi_ids):
    # given
    result = None

    def producer_test_func(context, queue, fi_id):
        queue.put({
            "fi_id": fi_id,
            "data": "filler"
        })

    def consumer_test_func(context, client, msg):
        nonlocal result

        data = msg["data"]
        fi_id = msg["fi_id"]

        result = client.send(context, fi_id, data)

    cp = ProducerConsumer(context, mocked_client_401, one_valid_fi_ids)
    cp.add_producer("producer", producer_test_func)
    cp.set_consumer_func(consumer_test_func)
    cp.set_num_consumers(1)

    # when
    cp.run()

    # then
    assert 2 == len(mocked_client_401.datas)
    assert result
