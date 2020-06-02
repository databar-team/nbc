from collections import OrderedDict

from kasasa_common.api.response_envelope import ResponseEnvelope

from config.context import ServiceContext, build_context
from config.shared_text import QueueKeys, ErrorMessages
from service.models.response import build_response
from util.queue.filesystem import FileSystemWorkQueue as WorkQueue


class ProductDataController:
    """
    ProductDataController controls requests on the `api/v1/product-data` endpoint.
    """
    def __init__(self, context: ServiceContext = None):
        if context is None:
            context = build_context('service')
        self.context = context
        self.work_queue = WorkQueue(self.context.WORK_QUEUE_CONTEXT)
        self.queue_key = QueueKeys.PRODUCT_DATA

    def post(self) -> (OrderedDict, int):
        """
        Routes the request to the correct queue method and returns the status code and error message as applicable.

        :return: (status_code: int, error: str)
        """
        success, error = self.work_queue.put(self.queue_key)
        if success:
            response, model = build_response('ok')
            return ResponseEnvelope(model).create_single_result_response(response), 201
        else:
            response = ResponseEnvelope(dict()).create_error_response(error)
            if error == ErrorMessages.LOCKED_EXISTS or error == ErrorMessages.UNLOCKED_EXISTS:
                return response, 409
            else:
                return response, 500


class ConnectionController:
    """
    ConnectionController controls requests on the `api/v1/admin/health/` endpoint.
    """    
    def __init__(self, context: ServiceContext = None):
        if context is None:
            context = build_context('service')
        self.context = context
        self.work_queue = WorkQueue(self.context.WORK_QUEUE_CONTEXT)
        self.queue_key = QueueKeys.PRODUCT_DATA

    def post(self) -> (OrderedDict, int):
        """
        Routes the request to the correct queue method and returns the status code and error message as applicable.

        :return: (status_code: int, error: str)
        """
        success, error = self.work_queue.put(self.queue_key)
        if success:
            response, model = build_response('ok')
            return ResponseEnvelope(model).create_single_result_response(response), 200


class WorkerProcessController:
    """
    WorkerProcessController controls requests on the `api/v1/admin/ready/` endpoint.
    """    
    def __init__(self, context: ServiceContext = None):
        if context is None:
            context = build_context('service')
        self.context = context
        self.work_queue = WorkQueue(self.context.WORK_QUEUE_CONTEXT)
        self.queue_key = QueueKeys.PRODUCT_DATA

    def post(self) -> (OrderedDict, int):
        """
        Routes the request to the correct queue method and returns the status code and error message as applicable.

        :return: (status_code: int, error: str)
        """
        success, error = self.work_queue.put(self.queue_key)
        if success:
            response, model = build_response('ok')
            return ResponseEnvelope(model).create_single_result_response(response), 200
        else:
            response = ResponseEnvelope(dict()).create_error_response(error)
            if error == ErrorMessages.LOCKED_EXISTS or error == ErrorMessages.UNLOCKED_EXISTS:
                return response, 500
            else:
                return response, 503