import threading
from time import sleep

from kasasa_common.concurrency import ProducerConsumer
from kasasa_common.database import get_connection_object
from kasasa_common.logger import logger

from config.context import WorkerContext
from config.shared_text import QueueKeys
from util.queue.filesystem import FileSystemWorkQueue
from worker.manager.producers import ProductDataProducer
from worker.manager.consumers import ProductDataConsumer


class WorkManager:
    """
    WorkManager is a mediator between the work requested by the API and the ProducerConsumer that
    handles the work.

    Producers and Consumers should be defined as a child of worker.manager.producers.Producer and
    worker.manager.consumers.Consumer and then instantiated with any instance specific configurations.
    They are registered to the WorkManager using the structure defined in this classes __init__.

    WorkManager will only spawn producer threads for work that has been requested through the API
    and will add additional work to the ProducerConsumer if that work is picked up before the
    thread at `self.producer_consumer_thread` dies or is shutting down.
    """
    def __init__(self, context: WorkerContext, work_queue: FileSystemWorkQueue):
        self.context = context
        self.reader = get_connection_object(self.context.READER_CONTEXT)
        self.reader.close()
        self.writer = get_connection_object(self.context.WRITER_CONTEXT)
        self.writer.close()
        self.producers = {
            QueueKeys.PRODUCT_DATA: dict(
                instance=ProductDataProducer(context.MARKETING_CLOUD_CONTEXT)
            )
        }
        self.consumers = {
            QueueKeys.PRODUCT_DATA: dict(
                instance=ProductDataConsumer(reader=self.reader, writer=self.writer)
            )
        }
        self.producer_consumer = None
        self.producer_consumer_thread = None
        self.work_queue = work_queue
        self.time_to_wait = 10

    def run(self):
        """
        run is responsible for the flow WorkManager. It iterates as long as there is work being processed
        and will shutdown when either the work is complete or no work has been picked up.

        If new work is found while the ProducerConsumer is still running, run will add it to the work being
        done. Otherwise, if ProducerConsumer is finishing up, run will return the work to the queue.

        If no work is found, the loop should break.

        :return:
        """
        logger.info('WorkManager has started...')
        while True:
            work = self.work_queue.get()
            if work is not None:
                if not self.producer_consumer:
                    self.build_producer_consumer()
                self.register_producer_for_work(work)
                if self.producer_consumer_thread and self.producer_consumer_thread.is_alive():
                    if not self.producer_consumer.event_manager.is_set():
                        event = self.producer_consumer.event_manager.get(work, None)
                        if event is None or event.is_set():
                            self.producer_consumer.start_producer(work)
                        else:
                            logger.warn(f"Somehow received {work} work while already processing that work")
                    else:
                        logger.warn("ProducerConsumer thread is already shutting down, replacing work in queue")
                        self.work_queue.reset_work(work)
                        break
                else:
                    self.start_producer_consumer()
            if self.producer_consumer_thread is None:
                break
            elif not self.producer_consumer_thread.is_alive():
                logger.info("ProducerConsumer is dead, shutting down WorkManager")
                break
            logger.debug("Waiting for 10 seconds before checking for more work")
            sleep(self.time_to_wait)

    def build_producer_consumer(self):
        """Instantiates the ProducerConsumer and registers the consumers to it"""
        self.producer_consumer = ProducerConsumer(self.context.PRODUCER_CONSUMER_CONTEXT)
        self.register_consumers()

    def register_producer_for_work(self, work: str):
        """Registers the producer that is relevant to the work being requested"""
        producer = self.producers.get(work, None)
        if producer is None:
            logger.error(f"Tried to register a producer that does not exist; {work}")
        self.producer_consumer.register_producer(
            name=work,
            producer_func=producer['instance'].producer_func,
            producer_args=producer.get('args', ()),
            producer_kwargs=producer.get('kwargs', dict())
        )

    def register_consumers(self):
        """Registers all consumers to the ProducerConsumer instance"""
        for name, consumer in self.consumers.items():
            self.producer_consumer.register_consumer(
                name=name,
                consumer_func=consumer['instance'].consumer_func,
                consumer_args=consumer.get('args', ()),
                consumer_kwargs=consumer.get('kwargs', dict())
            )

    def start_producer_consumer(self):
        """Starts the ProducerConsumer and registers it's thread"""
        self.producer_consumer_thread = threading.Thread(
            name="producer_consumer",
            target=self.producer_consumer.run
        )
        self.producer_consumer_thread.start()
