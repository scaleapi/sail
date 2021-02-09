import requests
from requests.auth import HTTPBasicAuth
from concurrent.futures import ThreadPoolExecutor


class Sail:
    def __init__(self, api_key, concurrency_limit=30, num_retries=3):
        self.api_key = api_key
        self.concurrency_limit = concurrency_limit
        self.num_retries = num_retries

    def request(self, method, url, json=None):
        return requests.request(
            method=method,
            url=url,
            json=json,
            headers={"Content-Type": "application/json"},
            auth=(self.api_key, ''))

    def get_project(self, name):
        return self.request("GET", f"https://api.scale.com/v1/projects/{name}")

    def get_batch(self, name):
        return self.request("GET", f"https://api.scale.com/v1/batches/{name}")

    def create_project(self, payload):
        return self.request("POST", f"https://api.scale.com/v1/projects/", payload)

    def create_batch(self, payload):
        return self.request("POST", f"https://api.scale.com/v1/batches/", payload)

    def create_task(self, type, payload):
        return self.request("POST", f"https://api.scale.com/v1/task/{type}/", payload)

    def finalize_batch(self, name):
        return self.request("POST", f"https://api.scale.com/v1/batches/{name}/finalize")

    def execute(self, fn, values):
        counter = 0
        with ThreadPoolExecutor(max_workers=self.concurrency_limit) as executor:
            for output in executor.map(fn, values):
                counter += 1
                print(f"{'{:6d}'.format(counter)}/{len(values)} | {output}")
