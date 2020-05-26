import json
import threading
import requests
from util.logger import logger

RETRY_LIMIT = 2

class MarketingCloudClient:
    
    def __init__(self):
        self.access_token_lock = threading.Lock()
        self.successful_fis_lock = threading.Lock()
        self.access_token = None
        self.successful_fis = []

    def set_access_token(self, context):
        with self.access_token_lock:
            logger.info("Getting access token.")

            body = {
                "grant_type": "client_credentials",
                "client_id": context.MC_AUTH_ID,
                "client_secret": context.MC_AUTH_SECRET
            }

            r = requests.post(context.MC_AUTH_URL, data=body)

            if r.status_code != 200:
                logger.info("Failed getting access token.")
                return

            data = r.json()

            self.access_token = data["access_token"]

    def send(self, context, fi_id, data):
        retries = 0
        success = False

        while retries <= RETRY_LIMIT:
            response = self._make_request(context, fi_id, data)

            if response.status_code == 200:
                success = True
                break
            elif response.status_code == 401:
                logger.info("Invalid access token, retrying.")

                # if another thread is getting a token,
                # then don't try to get a new token and wait
                if self.access_token_lock.locked():
                    while self.access_token_lock.locked():
                        pass
                else:
                    self.set_access_token(context)

                retries += 1
                continue
            else:
                logger.error(response.text)
                logger.info("Failed to send payload to {url}".format(url=context.MC_REST_URL.format(fi_id)))
                break

        if not success:
            logger.error("Error with batch send to marketing cloud.")
        else:
            with self.successful_fis_lock:
                if fi_id not in self.successful_fis:
                    self.successful_fis.append(fi_id)

        return success

    def _make_request(self, context, fi_id, data):
        access_token = self.access_token

        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(access_token)
        }

        req = requests.Request('POST', context.MC_REST_URL.format(fi_id), data=json.dumps(data), headers=headers)
        preq = req.prepare()

        sess = requests.Session()

        return sess.send(preq, timeout=30)