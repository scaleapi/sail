import json
import concurrent.futures
import threading
import os

import schema_validation
import project
import batch
import task
import client

schema = {
    "project": {
        "name": "Insert Test 2", # Required
        "type": "imageannotation", # Required
        "instruction": "Do the other thing", # Required
        "callback_url": "https://www.example.com/callback", # Required, but can be just "https://www.example.com/callback"
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

def main():
    # Specify your API Key, live_xxxxxxxxx
    if 'API_KEY' not in os.environ:
        raise(Exception(f"Missing `API_KEY` as Environment Variable"))

    # Create a Sail client to handle making requests to Scale
    sail_client = client.Sail(os.environ["API_KEY"])

    # Validate that the schema is valid
    schema_validation.validate_schema(schema)

    # Get or Create the Project
    project.upsert(sail_client, schema['project'])

    # If we're using batches, create them
    if ('batches' in schema):
        batch.upsert(sail_client, schema['project']['name'], schema['batches'])

    # Create all tasks specified
    task.create(sail_client, schema['project'], schema.get('batches', None), schema['tasks'])

    # If we were using batches and we want to finalized them, do so
    if ('batches' in schema and schema['batches'].get('finalizeBatchAfterSubmission', True)):
        batch.finalize(sail_client, schema['batches'])

if __name__ == "__main__":
    main()


## TODOS:
# Add Timeout + Try/Catch to Requests
# Add Timers (Start/Stop) to batches and task creation