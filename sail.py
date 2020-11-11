import requests
from requests.auth import HTTPBasicAuth
import json
import concurrent.futures
import threading
import os

import schema_validation
import project
import batch
import task

CONCURRENCY_LIMIT = 30

schema = {
    "project": {
        "name": "Insert Test 2", # Required
        "type": "imageannotation", # Required
        "instruction": "Do the other thing", # Required
        "callback_url": "https://www.example.com/callback", # Required
        "geometries": {
            "box": {
                "objects_to_annotate": ["Bike", "Cool Car"]
            }
        }
    },
    "batches": { # If creating more than 1 batch, you need to specify the batch name in the task params
        "batches": [
            {
                "name": "Batch1", # Required
                "callback_url": "https://www.example.com/callback" #Optional
            },
            {
                "name": "Batch2", # Required
                "callback_url": "https://www.example.com/callback" #Optional
            },
            {
                "name": "Batch3", # Required
                "callback_url": "https://www.example.com/callback" #Optional
            },
            {
                "name": "Batch4", # Required
                "callback_url": "https://www.example.com/callback" #Optional
            },
            {
                "name": "Batch5", # Required
                "callback_url": "https://www.example.com/callback" #Optional
            },
            {
                "name": "Batch6", # Required
                "callback_url": "https://www.example.com/callback" #Optional
            },
        ],
        "finalizeBatchAfterSubmission": True, # Setting to True will disallow future tasks to be submitted to this same batch
        "batchStatusOverride": True, #  Unless instructed otherwise, leave it set to be False :)
    },
    "tasks": {
        "list": [
            {
                "attachment": "https://media4.s-nbcnews.com/i/newscms/2020_08/3241236/200223-chevy-c8-cs-158p_ee63ca035f5144382d5dbbe3aea81192.jpg"
            }
        ],
        "csv": [
            {
                "filename": "example_schemas/CSV/task_data.csv"
            }
        ],
        "useIdempotency": True # Recommended safety precaution to avoid duplicates
    }
}

class SailClient:
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

def main():
    if 'API_KEY' not in os.environ:
        raise(Exception(f"Missing `API_KEY` as Environment Variable"))

    client = SailClient(os.environ["API_KEY"], CONCURRENCY_LIMIT)

    schema_validation.validate_schema(schema)

    project.upsert(client, schema['project'])

    if ('batches' in schema):
        batch.upsert(client, schema['project']['name'], schema['batches'])

    task.create(client, schema['project'], schema.get('batches', None), schema['tasks'])

    if ('batches' in schema and schema['batches'].get('finalizeBatchAfterSubmission', True)):
        batch.finalize(client, schema['batches'])

if __name__ == "__main__":
    main()


## TODOS:
# Add Timeout + Try/Catch to Requests
# Add Timers (Start/Stop) to batches and task creation