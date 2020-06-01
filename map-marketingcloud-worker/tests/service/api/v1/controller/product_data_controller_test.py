import pytest

from config.context import ServiceContext, WorkQueueContext
from service.api.v1.controller.product_data_controller import ProductDataController


@pytest.fixture
def test_context():
    work_queue_path = './test_queue/{}'
    work_queue_context = WorkQueueContext(PATH=work_queue_path, TYPE='filesystem')

    context = ServiceContext(WORK_QUEUE_CONTEXT=work_queue_context)
    yield context

    import shutil
    shutil.rmtree(work_queue_context.PATH, ignore_errors=True)


def test_product_data_controller_post_successful(test_context):
    # Given
    expected = ({"data": {"message": "ok"}}, 201)
    test_context.WORK_QUEUE_CONTEXT.PATH = test_context.WORK_QUEUE_CONTEXT.PATH.format(
        "test_product_data_controller_post_successful"
    )
    pdc = ProductDataController(test_context)

    # When
    actual = pdc.post()

    # Then
    assert actual == expected


def test_product_data_controller_post_second_attempt_fails(test_context):
    # Given
    expected = ({"error": {"message": "unlocked item already exists"}}, 409)
    test_context.WORK_QUEUE_CONTEXT.PATH = test_context.WORK_QUEUE_CONTEXT.PATH.format(
        "test_product_data_controller_post_second_attempt_fails"
    )
    pdc = ProductDataController(test_context)

    # When
    pdc.post()
    actual = pdc.post()

    # Then
    assert actual == expected


def test_product_data_controller_post_attempt_on_locked_item_fails(test_context):
    # Given
    expected = ({"error": {"message": "locked item already exists"}}, 409)
    test_context.WORK_QUEUE_CONTEXT.PATH = test_context.WORK_QUEUE_CONTEXT.PATH.format(
        "test_product_data_controller_post_attempt_on_locked_item_fails"
    )
    pdc = ProductDataController(test_context)

    # When
    pdc.work_queue.put("product-data.lock")
    actual = pdc.post()

    # Then
    assert actual == expected
