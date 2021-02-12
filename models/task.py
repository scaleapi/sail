import csv
import json


def create(client, project, batches, tasks):
    print("\n\nCreating Tasks...")
    print("=================")

    tasks_to_create = []

    # Load tasks from the schema list
    if ('list' in tasks):
        tasks_to_create.extend(tasks['list'])

    # Load tasks from CSV files
    if ('csv' in tasks):
        for filename in tasks['csv']:
            tasks_to_create.extend(csv.DictReader(open(filename)))

    # Load tasks from JSON files
    if ('json' in tasks):
        for filename in tasks['json']:
            tasks_to_create.extend(json.load(open(filename)))

    # TODO: Add support for folder import

    def create_task(task, num_retries=3):

        attachment = task.get('attachment', task.get('attachments'))

        # Add project
        task['project'] = project['name']

        # If applicable, add batch
        if batches is not None and len(batches['batches']) == 1:
            task['batch'] = batches['batches'][0]['name']

        # If applicable, add unique_id
        if not task.get('unique_id') and tasks.get('generateUniqueId', False):
            if task.get('batch'):
                task['unique_id'] = f"{task['project']}_{task['batch']}_{attachment}"
            else:
                task['unique_id'] = f"{task['project']}_{attachment}"

        # Try and create the task
        res = client.create_task(project['type'], task)

        # See if we were successful
        if (res.status_code == 200):
            task_res = res.json()
            return f"✅ Successfully created task {task_res['task_id']} with attachment '{attachment}'"

        elif (res.status_code == 409):
            return f"✅ Task with unique_id '{task['unique_id']}' already exists, skipping"

        else:
            return f"❌ Task creation for '{attachment}' failed with response {res.json()}"

    client.execute(create_task, tasks_to_create)
