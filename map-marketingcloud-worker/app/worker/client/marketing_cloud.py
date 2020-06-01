import json
import threading
import requests
from datetime import datetime, timedelta

from kasasa_common.logger import logger

from config.context import MarketingCloudClientContext


RETRY_LIMIT = 2


class MarketingCloudClient:
    
    def __init__(self):
        self.access_token_lock = threading.Lock()
        self.successful_fis_lock = threading.Lock()
        self.access_token = None
        self.request_id = None
        self.todays_date = datetime.today()
        self.yesterdays_date = self.todays_date - timedelta(1)

    def set_access_token(self, context: MarketingCloudClientContext):
        """
        set_access_token will reach out to the auth url and fetch the access token for the session, then set it to be
        available to this instance of the class.

        :param context: MarketingCloudClientContext object
        :return:
        """
        with self.access_token_lock:
            logger.info("Getting access token.")

            body = {
                "grant_type": "client_credentials",
                "client_id": context.AUTH_ID,
                "client_secret": context.SECRETS.get(context.AUTH_SECRET_KEY)
            }

            r = requests.post(context.AUTH_URL, data=body)

            if r.status_code != 200:
                logger.info("Failed getting access token.")
                return

            data = r.json()

            self.access_token = data["access_token"]

    def fetch_product_data(self, context):
        """
        fetch_product_data fetches from Marketing Cloud, the previous days updates. In the event that more records exist
        that were not returned in the first call, calling this method again will return the next results until there
        are no more results to fetch.

        :param context: MarketingCloudClientContext object
        :return (list, bool): results from the call and the value of HasMoreRows if it exists
        """
        retries = 0
        success = False
        content = dict()
        while retries <= RETRY_LIMIT:
            response = self._fetch_product_data(context)

            if response.status_code == 200:
                if hasattr(response, 'content'):
                    try:
                        content = response.json()
                    except json.decoder.JSONDecodeError:
                        # The main reason this will happen is an invalid access token and the endpoint
                        # returning nothing parsable in the content.

                        # This could also be because an error was returned as the content. But we cannot log the content
                        # because of potentially sensitive information being included.

                        # wait if another thread is setting the access token already
                        if self.access_token_lock.locked():
                            while self.access_token_lock.locked():
                                pass
                        else:
                            self.set_access_token(context)
                        retries += 1
                        continue
                    else:
                        success = True
                        break
            else:
                logger.error(response.text)
                logger.info("Failed to send payload to {url}".format(url=context.GET_PRODUCT_DATA_URL))
                break

        if not success:
            logger.error("Error fetching product data from marketing cloud")

        self.request_id = content.get("RequestID", None)
        has_more_rows = content.get('HasMoreRows', False)
        if not has_more_rows:
            self.request_id = None
        return content.get('Results', []), has_more_rows

    def _fetch_product_data(self, context: MarketingCloudClientContext):
        """
        :return response: response object
        """
        payload = {
            "Token": self.access_token,
            "Method": "getMarketingProductDetails",
            "startDate": self.yesterdays_date.strftime('%Y-%m-%d'),
            "endDate": self.todays_date.strftime('%Y-%m-%d')
        }

        if self.request_id is not None:
            payload["RequestID"] = self.request_id

        headers = {
            'Content-Type': 'application/json'
        }

        req = requests.Request('POST', context.GET_PRODUCT_DATA_URL, data=json.dumps(payload), headers=headers)
        prepared_req = req.prepare()

        session = requests.Session()

        return session.send(prepared_req, timeout=30)
