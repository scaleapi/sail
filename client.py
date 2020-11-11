import requests
from requests.auth import HTTPBasicAuth

class Sail:
    def __init__(self, api_key, concurrency_limit):
        self.api_key = api_key
        self.concurrency_limit = concurrency_limit
    
    def makeScaleRequest(self, method, url, custom_headers={}, json=None):
        
        auth = HTTPBasicAuth(self.api_key, '')
        headers = {
            "Content-Type": "application/json",
        }
        headers = {**headers, **custom_headers}

        return requests.request(
            method, url=url, json=json, headers=headers, auth=auth
        )