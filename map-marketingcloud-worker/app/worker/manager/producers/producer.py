import queue
from time import sleep
from typing import Any

from kasasa_common.queue import QueueInterface
from kasasa_common.logger import logger


class Producer:
    def __init__(self, job_type: str):
        self.job_type = job_type

    def add_to_queue(self, work_queue: QueueInterface, payload: Any) -> bool:
        """Adds the payload to the given queue with the proper dictionary config"""
        data = dict(
            job_type=self.job_type,
            payload=payload
        )
        while True:
            try:
                work_queue.put(data)
                return True
            except queue.Full:
                sleep(1)
            except Exception:
                logger.exception('Failed to put data on the worker queue')
                return False

    def producer_func(self, work_queue: QueueInterface, *args, **kwargs):
        return self._producer_func(work_queue, *args, **kwargs)

    def _producer_func(self, work_queue, *args, **kwargs):
        raise NotImplementedError
