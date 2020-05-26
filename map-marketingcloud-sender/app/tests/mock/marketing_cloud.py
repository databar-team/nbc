import requests
import threading
from client.marketing_cloud import MarketingCloudClient

class MockMarketingCloudClient(MarketingCloudClient):

    def __init__(self):
        super().__init__()

        self.datas = []
        self.fi_ids = []
        self.mocked_responses = []

    def add_mocked_response(self, response):
        self.mocked_responses.append(response)

    def set_access_token(self, context):
        self.access_token = "foobar"

    def _make_request(self, context, fi_id, data):
        if fi_id not in self.fi_ids:
            self.fi_ids.append(fi_id)

        self.datas.append(data)

        if len(self.mocked_responses) > 0:
            return self.mocked_responses.pop(0)
        
        response = requests.Response
        response.status_code = 500
        return response

class MockResponse(object):

    def __init__(self):
        self.status_code = 0