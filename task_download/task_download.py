import argparse
import requests
import json
import os
import logging
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

# constants
BATCH_URL = 'https://api.scale.com/v1/batches'
TASK_URL = 'https://api.scale.com/v1/tasks'
MAX_WORKERS = 200

# globals
auth = None
batch_total = 0
batch_count = 0
task_count = 0
error_batches = []
path = os.path.dirname(__file__)

# create logs and batches directories
if not os.path.isdir(f'{path}/logs'):
    os.mkdir(f'{path}/logs')

if not os.path.isdir(f'{path}/batches'):
    os.mkdir(f'{path}/batches')

# logger
logging.basicConfig(format='%(levelname)s %(message)s', level=logging.INFO)
info = logging.info
error = logging.error
logger = logging.getLogger()
logger.addHandler(logging.FileHandler(
    f'{path}/logs/{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'))


def main():
    global batch_total, auth

    args = get_args()
    auth = (args.api_key, '')
    resume = args.resume

    batches = get_batches()
    batch_total = len(batches)

    info(f'Downloading {batch_total} batches...')

    futures = []
    threadpool = ThreadPoolExecutor(max_workers=MAX_WORKERS)
    for batch in batches:
        if resume and os.path.isfile(f'{path}/batches/{batch}.json'):
            batch_total -= 1
            info(f'Skipping batch {batch} since --resume flag was used')
        else:
            future = threadpool.submit(get_tasks, batch)
            futures.append(future)

    for future in futures:
        future.result()

    if(len(error_batches)):
        error(f'Error batches: {error_batches}')
        error(
            f'There were errors downloading {len(error_batches)} batches, to retry run the script with the --resume flag')


def get_batches():
    batches = []
    has_next_page = True
    next_page = 1
    info('Getting batch pages...')
    try:
        while(has_next_page):
            params = {'status': 'completed', 'offset': (next_page - 1) * 100}
            res = requests.get(BATCH_URL, auth=auth, params=params).json()

            info(f'Getting batch page {next_page}/{res.get("totalPages")}')

            has_next_page = res.get('hasNextPage')
            next_page = res.get('nextPage')

            for batch in res.get('docs'):
                batches.append(batch['name'])
    except Exception:
        logging.exception(
            "Exception occurred while downloading batch pages, please try again")
        quit()

    return batches


def get_tasks(batch):
    global batch_count, task_count, error_batches

    file_name = f'{path}/batches/{batch}.json'
    next_token = True

    try:

        with open(file_name, "w") as f:
            f.write('[')
            if(batch == 'Io_Pilot_2_Batch_1_100_Elec_App_Sports_Music_Decor'):
                raise Exception('Upss')
            while next_token:
                params = {
                    'next_token': '' if next_token == True else next_token,
                    'batch': batch
                }
                res = requests.get(TASK_URL, auth=auth, params=params).json()

                next_token = res.get('next_token')
                tasks = res.get('docs')
                task_count += len(tasks)

                for task in tasks:
                    f.write(f'{json.dumps(task, indent=2)},')

            f.write(']')

        batch_count += 1

        info(
            f'Finished batch {batch} ({batch_count}/{batch_total}) | Task sum: {task_count}')
    except Exception:
        if os.path.isfile(file_name):
            os.remove(file_name)
        logging.exception(
            f'Exception occurred while downloading batch {batch}')
        error_batches.append(batch)


def get_args():
    ap = argparse.ArgumentParser()
    ap.add_argument('--api-key', required=True)
    ap.add_argument('--resume', action='store_true')
    return ap.parse_args()


if __name__ == "__main__":
    main()
