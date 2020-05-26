import threading, queue
from time import sleep

from concurrency.event_manager import EventManager
from util.logger import logger


class ProducerConsumer:
    def __init__(self, context, client, fi_ids):
        self.context = context
        self.client = client
        self.fi_ids = fi_ids
        self.event_manager = EventManager()
        self.queue = queue.Queue(maxsize=30)

        self.consumer_func = None
        self.num_consumers = 5
        self.producers = {}
        self.consumers = []
        self.thread_exception_list = []
        self._exception_list_lock = threading.Lock()

    def add_producer(self, name, producer_func):
        self.producers[name] = producer_func

    def set_consumer_func(self, consumer_func):
        self.consumer_func = consumer_func

    def set_num_consumers(self, num_consumers):
        self.num_consumers = num_consumers

    def run(self):
        threads = []

        for name, producer_func in self.producers.items():
            self.event_manager.add_event(name)
            thread = threading.Thread(name=name, target=self.__producer, args=(producer_func,))
            threads.append(thread)
            thread.start()

        num = 0
        while num < self.num_consumers:
            thread = threading.Thread(name="consumer_{}".format(num+1), target=self.__consumer, args=(self.consumer_func,))
            threads.append(thread)
            thread.start()
            num += 1

        for t in threads:
            t.join()

        self.queue.join()

        logger.info(f"completed work, {len(self.thread_exception_list)} exceptions were encountered. "
                    f"{self.thread_exception_list if len(self.thread_exception_list) > 0 else ''}")

    def __producer(self, producer_func):
        for fi_id in self.fi_ids:
            try:
                producer_func(self.context, self.queue, fi_id)
            except Exception as e:
                name = threading.current_thread().getName()
                logger.error(f"Thread {name} encountered an unhandled exception in producer function: {e}",
                             exc_info=True)
                with self._exception_list_lock:
                    self.thread_exception_list.append(e)

        # notify consuming threads we are done
        logger.info("Finished {}".format(threading.current_thread().getName()))

        self.event_manager.set(threading.current_thread().getName())

    def __consumer(self, consumer_func):
        while not self.queue.empty() or not self.event_manager.is_set():
            try:
                msg = self.queue.get_nowait()

                consumer_func(self.context, self.client, msg)

                self.queue.task_done()
            except queue.Empty:
                sleep(1)
            except Exception as e:
                name = threading.current_thread().getName()
                logger.error(f"Thread {name} encountered an unhandled exception on consumer function: {e}",
                             exc_info=True)
                with self._exception_list_lock:
                    self.thread_exception_list.append(e)
                self.queue.task_done()
                continue

        logger.info("Finished {}".format(threading.current_thread().getName()))