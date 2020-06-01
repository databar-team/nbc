from kasasa_common.database.connection import Connection
from kasasa_common.logger import logger
from worker.manager.consumers.consumer import Consumer
from worker.data.fi_mc import FiMarketingCloud


class ProductDataConsumer(Consumer):
    def __init__(self, reader: Connection, writer: Connection):
        """
        Controlling class for a consumer of Product Data type work
        :param reader:
        :param writer:
        """
        self.reader: Connection = reader
        self.writer: Connection = writer

    def _consumer_func(self, payload, *args, **kwargs):
        mc_fi_db = FiMarketingCloud(self.writer)
        inserted = mc_fi_db.insert_many(values=payload['product_data'], fi_id=f"fi_{payload['fi_id']}", on_duplicate_key_update=True)
        logger.info(f"{inserted} records inserted in FI {payload['fi_id']}")
        return payload['fi_id'], inserted
