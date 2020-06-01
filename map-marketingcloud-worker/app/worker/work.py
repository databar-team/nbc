from time import sleep

from config.context import build_context
from util.queue.filesystem import FileSystemWorkQueue
from worker.manager.work_manager import WorkManager


def main():
    """
    Iterate forever and sleep for the configured time between iterations.
    If there is work to be processed, start a WorkManager.

    :return:
    """
    context = build_context('worker')
    work_queue = FileSystemWorkQueue(context.WORK_QUEUE_CONTEXT)
    while True:
        if not work_queue.empty:
            WorkManager(context, work_queue).run()
        sleep(context.SLEEP_TIME)


if __name__ == '__main__':
    main()
