import csv
import scaleapi
from scaleapi.tasks import TaskType
from scaleapi.api import Api
from scaleapi import exceptions
from helpers.concurrency import execute
from models import project, batch, task

# This file provides starter code to create a batch of tasks in a Rapid project

api_key = '' # Put your own API Key here
client = scaleapi.ScaleClient(api_key)

task_type = TaskType.ImageAnnotation
project_name = ''
batch_name = ''
csv_filepath = '' # csv with attachment_url column

def create_rapid_task(payload):
    # create the task
    try:
        new_task = client.create_task(task_type, **payload)
        return f"✅ Successfully created task {new_task.id} with attachment '{payload['attachment']}'"

    except exceptions.ScaleException as err:
        return f"❌ Task creation for '{payload['attachment']}' failed <Status Code {err.code}: {err.message}>"

def main():
    print("\n\nCreating Batch...")
    batch = client.create_batch(project=project_name, batch_name=batch_name)
    print(f"Batch {batch.name} created")

    # build task payloads
    task_payloads = []
    with open(csv_filepath, 'r') as csvfile:
        csvreader = csv.reader(csvfile)

        # skip header
        next(csvreader)

        for row in csvreader:
            task_payloads.append(
              dict(
                project = project_name,
                attachment_type = 'image',
                attachment = row[0],
                batch = batch_name
              )
            )
    
    print("\n\nCreating Tasks...")
    execute(create_rapid_task, task_payloads)

    client.finalize_batch(batch_name)
    print(f"Batch {batch.name} finalized")

if __name__ == "__main__":
    print("")
    main()
    print("\n")