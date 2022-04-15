schema = {
    "project": {
        # Required
        "name": "Test Project 33",
        # Required, the task type for all tasks in this project
        "type": "imageannotation",
        # Required, can use plain text, Markdown, or an embedded Google Doc
        "instruction": "Mark all bikes and cars on the image",
        
        # Example, Geometries to annotate on the task attachment image
        "geometries": {
            "box": {
                "objects_to_annotate": [
                    "Bike",
                    "Car",
                ]
            }
        }
    },
    #
    # Task payload are loaded from this list, plus the CSV and JSON files
    "tasks": {
        "list": [
            {
                # The url of the attachment to work on
                "attachment": "https://media4.s-nbcnews.com/i/newscms/2020_08/3241236/200223-chevy-c8-cs-158p_ee63ca035f5144382d5dbbe3aea81192.jpg?asd",
            }
        ],
        "csv": ["example_schemas/tasks.csv"],
        "json": ["example_schemas/tasks.json"],
        # If set to True, a unique_id will be generated for each task. Recommended to avoid duplicates.
        "generateUniqueId": True
    }
}
