schema = {
    "project": {
        # Required
        "name": "Test Project 33",
        # Required, the task type for this project
        "type": "imageannotation",
        # Required, can use text, markdown, or embedded google doc
        "instruction": "Mark all bikes and cars on the image",
        # Required, but can be just "https://www.example.com/callback"
        "callback_url": "https://www.example.com/callback",
        # Geometries to annotatie in the attachment image
        "geometries": {
            "box": {
                "objects_to_annotate": [
                    "Bike",
                    "Car",
                    "Pedestrians"
                ]
            }
        }
    },
    #
    # If creating only one batch, all tasks will be created using this batch
    # If creating more than one batch, you need to specify the batch name in the task params
    "batches": {
        "batches": [
            {
                "name": "Test Project 33_batch_1",  # Required
                "callback_url": "https://www.example.com/callback"  # Optional
            },
            {
                "name": "Test Project 33_batch_2",  # Required
                "callback_url": "https://www.example.com/callback"  # Optional
            },
            {
                "name": "Test Project 33_batch_3",  # Required
                "callback_url": "https://www.example.com/callback"  # Optional
            }
        ],
        # Setting to True will disallow future tasks to be submitted to this same batch
        "finalizeBatchAfterSubmission": True,
        # Unless instructed otherwise, leave it set to be False :)
        "batchStatusOverride": True,
    },
    #
    # Task payload are loaded from this list, plus the CSV and JSON files
    "tasks": {
        "list": [
            {
                # If creating more than one batch, you need to specify the batch for each task here
                "batch": "Test Project 33_batch_1",
                # The url of the attachment to work on
                "attachment": "https://media4.s-nbcnews.com/i/newscms/2020_08/3241236/200223-chevy-c8-cs-158p_ee63ca035f5144382d5dbbe3aea81192.jpg?asd",
                # You can specify it here, or use the flag below instead
                "unique_id": "Insert Test 2_Task 1"
            }
        ],
        "csv": [
            "example_schemas/tasks.csv"
        ],
        "json": [
            "example_schemas/tasks.json"
        ],
        # Recommended safety precaution to avoid duplicates.
        # If set to True, a unique_id will be generated for each task
        "generateUniqueId": True
    }
}
