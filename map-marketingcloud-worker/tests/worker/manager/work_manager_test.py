import shutil
from unittest.mock import patch

import pytest
from kasasa_common import logger
from kasasa_common.concurrency import ProducerConsumer

from config.context import WorkerContext, WorkQueueContext
from worker.manager.work_manager import WorkManager
from worker.manager.consumers import Consumer
from worker.manager.producers import Producer
from util.queue.filesystem import FileSystemWorkQueue


@pytest.fixture
def test_queue_context():

    test_path = './test_queue/work_manager_test'

    return WorkQueueContext(
        TYPE='filesystem',
        PATH=test_path
    )


@pytest.fixture
def test_file_queue(test_queue_context):
    yield FileSystemWorkQueue(test_queue_context)
    shutil.rmtree(test_queue_context.PATH)


@pytest.fixture
def test_context(test_queue_context):
    return WorkerContext(
        WORK_QUEUE_CONTEXT=test_queue_context,
        WORKER_SLEEP_TIME=1
    )


@pytest.fixture
def mock_get_connection_object():
    mock_call_patcher = patch('worker.manager.work_manager.get_connection_object')
    mock_call = mock_call_patcher.start()

    yield mock_call

    mock_call_patcher.stop()


@pytest.fixture
def mock_connection_object():
    class Mocked:
        def close(self):
            pass
    return Mocked


@pytest.fixture
def test_work_manager(test_context, mock_get_connection_object, mock_connection_object):
    mock_get_connection_object.return_value = mock_get_connection_object()

    yield WorkManager(test_context, FileSystemWorkQueue(test_context.WORK_QUEUE_CONTEXT))


class Consumer1(Consumer):
    def _consumer_func(self, payload, *args, **kwargs):
        kwargs.get('append_to').append(payload)


class Consumer2(Consumer):
    def _consumer_func(self, payload, *args, **kwargs):
        logger.info(payload)


class Producer1(Producer):
    def __init__(self):
        super(Producer1, self).__init__('test_1')

    def _producer_func(self, work_queue, *args, **kwargs):
        self.add_to_queue(work_queue, "Producer1")


class Producer2(Producer):
    def __init__(self):
        super(Producer2, self).__init__('test_2')

    def _producer_func(self, work_queue, *args, **kwargs):
        self.add_to_queue(work_queue, "Producer2")


@pytest.fixture
def test_consumers():
    return dict(
        test_1=dict(instance=Consumer1()),
        test_2=dict(instance=Consumer2())
    )


@pytest.fixture
def test_producers():
    return dict(
        test_1=dict(instance=Producer1()),
        test_2=dict(instance=Producer2())
    )


def test_run(test_file_queue, test_work_manager: WorkManager, test_consumers, test_producers):
    # Given
    test_work_manager.work_queue = test_file_queue
    test_work_manager.producers = test_producers
    test_work_manager.consumers = test_consumers
    test_work_manager.time_to_wait = 0
    actual_result = []
    test_consumers['test_1']['kwargs'] = dict(append_to=actual_result)
    expected_result = ["Producer1"]

    # When
    test_file_queue.put('test_1')
    test_work_manager.run()

    # Then
    assert actual_result == expected_result


def test_build_producer_consumer(test_work_manager: WorkManager, test_consumers):
    # Given
    test_work_manager.consumers = test_consumers
    expected = 2

    # When
    test_work_manager.build_producer_consumer()
    actual = 0
    for name in test_consumers.keys():
        consumer = test_work_manager.producer_consumer.unregister_consumer(name)
        assert consumer['func'] == test_consumers[name]['instance'].consumer_func
        actual += 1

    # Then
    assert actual == expected


def test_register_producer_for_work(test_work_manager: WorkManager, test_producers):
    # Given
    test_work_manager.producers = test_producers
    expected = test_producers['test_1']['instance'].producer_func

    # When
    test_work_manager.build_producer_consumer()
    test_work_manager.register_producer_for_work('test_1')
    actual = test_work_manager.producer_consumer.unregister_producer('test_1')

    # Then
    assert actual['func'] == expected


def test_register_consumers(test_work_manager: WorkManager, test_consumers):
    # Given
    test_work_manager.consumers = test_consumers
    test_work_manager.producer_consumer = ProducerConsumer()
    expected = 2

    # When
    test_work_manager.register_consumers()
    actual = 0
    for name in test_consumers.keys():
        consumer = test_work_manager.producer_consumer.unregister_consumer(name)
        assert consumer['func'] == test_consumers[name]['instance'].consumer_func
        actual += 1

    # Then
    assert actual == expected
