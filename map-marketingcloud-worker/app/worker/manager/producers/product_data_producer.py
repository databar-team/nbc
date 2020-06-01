from datetime import datetime

from kasasa_common.logger import logger
from kasasa_common.queue import ThreadSafeQueueInterface

from config.context import MarketingCloudClientContext
from config.shared_text import QueueKeys
from worker.client.marketing_cloud import MarketingCloudClient
from worker.manager.producers.producer import Producer


class ProductDataProducer(Producer):
    """
    ProductDataProducer uses the MarketingCloudClient to reach out to the configured endpoint and feed results
    into the provided Work Queue.

    Example Put into queue:
    dict(
        job_type="product-data",
        payload=dict(
            fi_id=1234,
            payload=[
                {
                        "AcctProdIDFull__c": "a031I00002vIe0hQAC",
                        "AcctProductExternalID__c": "",
                        "Name": "RxSaver",
                        "Product Class": "Prescription Savings",
                        "Include for Cross Sell": "No",
                        "AccountNumber": "2327",
                        "Product__c": "",
                        "BillingKrpPid__c": "",
                        "Market_This_Product": "",
                        "Product_Priority": "",
                        "Opt-In_Status": ""
                },  # etc
            }
    )
    """
    def __init__(self, context: MarketingCloudClientContext):
        super(ProductDataProducer, self).__init__(job_type=QueueKeys.PRODUCT_DATA)
        self.context = context
        self.client = MarketingCloudClient()

    def _producer_func(self, work_queue: ThreadSafeQueueInterface, *args, **kwargs):
        start_time = datetime.now()
        has_more_rows = True
        self.client.set_access_token(self.context)
        while has_more_rows:
            result, has_more_rows = self.client.fetch_product_data(self.context)
            payload_map = dict()
            logger.info(f'Received {len(result)} records from Marketing Cloud')
            for item in result:
                self._update_map(item, payload_map)
            logger.info(f'Records grouped into {len(payload_map.keys())} FIs')
            for key in payload_map.keys():
                payload = dict(
                    fi_id=key,
                    product_data=payload_map[key]['product_data']
                )
                self.add_to_queue(work_queue, payload)
        end_time = datetime.now()
        logger.info(f'ProductDataProducer completed in {(end_time - start_time).seconds} seconds')

    @staticmethod
    def _update_map(item, payload_map):
        fi_id = item.get('AccountNumber', None)
        if fi_id is None:
            logger.error("one of the results had no AccountNumber value")
            return payload_map
        if payload_map.get(fi_id, None) is not None:
            payload_map[fi_id]['product_data'].append(item)
        else:
            payload_map[fi_id] = dict()
            payload_map[fi_id]['product_data'] = [item]
