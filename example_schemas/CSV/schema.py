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
        ],
        "finalizeBatchAfterSubmission": True, # Setting to True will disallow future tasks to be submitted to this same batch
        "batchStatusOverride": False, #  Unless instructed otherwise, leave it set to be False :)
    },
    "tasks": {
        "csv": [
            {
                "filename": "example_schemas/CSV/task_data.csv"
            }
        ],
        "useIdempotency": True # Recommended safety precaution to avoid duplicates
    }
}