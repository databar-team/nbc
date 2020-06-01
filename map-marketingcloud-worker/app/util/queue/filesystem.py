import os
import shutil
from pathlib import Path
from typing import Union

from kasasa_common.logger import logger

from config.context import WorkQueueContext
from config.shared_text import ErrorMessages


class FileSystemWorkQueue:
    """
    Very simple queue that lives on the file system. The goal is to allow the service and worker to communicate on
    what work needs to be completed.
    """
    def __init__(self, context: WorkQueueContext):
        self.context = context

    def put(self, key: str) -> (bool, str):
        """
        Given a key, enter an item in the queue. If the item already exists, either with a lock or without, a new item
        will not be added and False will be returned with the reason. If an item is created, True will be returned.

        :param key: name of item to add to queue
        :return: (success: bool, error: str)
        """
        return self._put_item(key)

    def get(self) -> Union[str, None]:
        """
        Returns the oldest filename in the queue path and sets it to lock status.

        If no file exists, None is returned.
        :return:
        """
        return self._get_item()

    def done(self, key: str) -> bool:
        return self._delete_item(key)

    def reset_work(self, key: str) -> bool:
        return self._reset_work(key)

    @property
    def empty(self) -> bool:
        return not self._work_exists()

    def _reset_work(self, key: str) -> bool:
        path = Path(self.context.PATH, f'{key}.lock')
        if not path.exists():
            logger.error(f"tried to reset a work item that does not exist: {key}")
            return False
        else:
            path.rename(f'{self.context.PATH}/{key}')
            return True

    def _put_item(self, key: str) -> (bool, str):
        if not Path(self.context.PATH).exists():
            logger.debug("Creating queue path")
            Path(self.context.PATH).mkdir(parents=True)
        if Path(self.context.PATH, f'{key}.lock').exists():
            logger.info("key exists in queue and is locked")
            return False, ErrorMessages.LOCKED_EXISTS
        path = Path(self.context.PATH, key)
        if path.exists():
            logger.info("key exists in queue and is unlocked")
            return False, ErrorMessages.UNLOCKED_EXISTS
        try:
            logger.info(f"attempting to create item for {key} in queue")
            path.touch()
        except Exception as e:
            logger.exception("Something unexpected happened when writing the file")
            return False, e
        return True, None

    def _get_item(self) -> Union[str, None]:
        path = Path(self.context.PATH)
        items = sorted(path.glob('*[!.lock]'), key=os.path.getmtime)
        if items:
            item = items.pop(0)
            name = item.name
            item.rename(f'{str(item.joinpath())}.lock')
            return name
        return None

    def _work_exists(self) -> bool:
        path = Path(self.context.PATH)
        items = sorted(path.glob('*[!.lock]'), key=os.path.getmtime)
        return len(items) > 0

    def _delete_item(self, key: str) -> bool:
        status = False
        path = Path(self.context.PATH)
        if not path.exists():
            logger.debug("Tried to delete item in directory that does not exist")
        else:
            count = 0
            for filename in path.glob(f'{key}*'):
                if filename.exists():
                    filename.unlink()
                count += 1
            if count > 0:
                status = True
        return status


__all__ = [FileSystemWorkQueue]
