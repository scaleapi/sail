# this is an example schema for creating a batch in an existing rapid project
schema = {
  "project": {
    "name": "", # fill in
    "type": "imageannotation",
  },
  "batches": {
    "batches": [
        {
            "name": "",   # fill in
        }
    ],
  },
  "tasks": {
    "csv": ["example_schemas/tasks.csv"], # populate csv file with your data
    "generateUniqueId": True
  }
}