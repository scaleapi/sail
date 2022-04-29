# Script that takes in an array of batch names (split by comma) and applies a bulk action to cancel all tasks in each batch.
# By default, this script makes 50 concurrent API calls.
from collections import defaultdict
import scaleapi
import argparse
from scaleapi.exceptions import ScaleException, ScaleUnauthorized
from concurrent.futures import ThreadPoolExecutor, as_completed

# Change this for update concurrency
MAX_WORKERS = 50 

def main():

    args = get_args()
    clearUniqueId = args.clear or False
    
    client = scaleapi.ScaleClient(args.api_key)
    
    # Test API Key
    try:
        client.projects()
    except ScaleUnauthorized as err:
        print(err.message)
        exit(1)

    preProcessedBatches = args.batches.split(",")
    batches = [word.strip() for word in preProcessedBatches]
    for batch_name in batches:
        processes = []

        print(f"\nProcessing Batch: {batch_name}")
        try:
            batch = client.get_batch(batch_name)
        except:
            print(f"-ERROR: Batch {batch_name} not found.")
            continue

        task_count = client.get_tasks_count(
            project_name = batch.project,
            batch_name = batch.name
        )
        print(f"-Batch {batch.name} contains {task_count} tasks.")

        summary_metrics = defaultdict(lambda:0)

        tasks = client.get_tasks(project_name = batch.project, batch_name = batch.name)
        task_in_progress = 0
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            
            for task in tasks:
                task_in_progress += 1
                if task_in_progress % 1000 == 0:
                    print(f"-Processing Task # {task_in_progress}")
                processes.append(executor.submit(cancel_task_with_response, client, task, clearUniqueId))
            
            for process in as_completed(processes):
                result = process.result()
                summary_metrics[result["status"]] += 1

        for k,v in summary_metrics.items():
            print(f"-{k}: {v} tasks")

def cancel_task_with_response(client: scaleapi.ScaleClient, task, clear_unique_ud):
    task_status = task.as_dict()["status"]
    if task_status in ['completed', 'canceled']:
        return {
            "task": task.id,
            "status": task_status
        }
    try:
        updated_task = client.cancel_task(task.id, clear_unique_ud)
        return {
            "task": task.id,
            "status": updated_task.as_dict()["status"]
        }
    except ScaleException: 
        return {
            "task": task.id,
            "status": "Can not cancel"
        }
    except Exception as err:
        print(err)

def get_args():
    ap = argparse.ArgumentParser()
    ap.add_argument('--api_key', required=True, help="Please provide Scale API Key")
    ap.add_argument('--batches', required=True, help="Please enter batch names separated by a comma")
    ap.add_argument('--clear', type=bool, help="Set to True if you want to remove unique_id upon cancel")
    return ap.parse_args()

if __name__ == "__main__":
    # Example: python cancelBatch.py --api_key "SCALE_API_KEY" --batches "batch1,batch2" --clear "True"
    main()
    
