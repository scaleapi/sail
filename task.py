import concurrent.futures
import threading
import csv

def create(client, project, batches, tasks):
    print("Creating Tasks...")

    tasks_to_create = []
    # Populate list of Tasks from List, .csv, a URL, etc.

    if ('list' in tasks):
        tasks_to_create.extend(tasks['list'])

    if ('csv' in tasks):
        for f in tasks['csv']:
            tasks_to_create.extend(csv.DictReader(open(f['filename'])))

    # TODO: Add support for .json import

    # TODO: Add support for folder import

    NUM_TASKS = len(tasks_to_create)

    def create_task(desired_task, num_retries = 3):

        # Add Project and if applicable, Batch Mapping
        desired_task['project'] = project['name']
        if batches is not None and len(batches['batches']) == 1:
            desired_task['batch'] = batches['batches'][0]['name']

        # Consider Idempotency
        #  - Goal is to build a unique key that represents this unit of work, may make sense to tweak given task type / other data
        custom_headers = {}
        if (tasks.get('useIdempotency', False)):
            key = f"{desired_task['project']}_{desired_task.get('batch','')}_{desired_task.get('attachment', desired_task.get('attachments'))}"
            custom_headers['Idempotency-Key'] = key.encode('utf-8')

        # Try and create the Task
        task_creation_res = client.makeScaleRequest("POST", f"https://api.scale.com/v1/task/{project['type']}/", json=desired_task, custom_headers=custom_headers)

        # See if we were successful
        if (task_creation_res.status_code == 200):
            task_res = task_creation_res.json()
            return f"Task `{task_res['task_id']}` has been created, attachment = {desired_task.get('attachment', desired_task.get('attachments'))}"
        elif (task_creation_res.status_code == 429):
            return f"Task `{desired_task['name']}` already exists based on Idempotency"
        else:
            # Try again if retry > 0
            if (num_retries > 0):
                print(f"Task creation for `{desired_task.get('attachment', desired_task.get('attachments'))}` failed with status code {task_creation_res.status_code}, trying {num_retries-1} more times")
                create_task(desired_task, num_retries-1)
            else: 
                raise(Exception(f"Exiting script, batch creation for {desired_task.get('attachment', desired_task.get('attachments'))} failed"))

    counter = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=client.concurrency_limit) as executor:
        for output in executor.map(create_task, tasks_to_create):
            counter += 1
            print(f"{'{:6d}'.format(counter)}/{NUM_TASKS} | {output}")