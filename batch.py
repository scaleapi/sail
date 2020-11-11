import concurrent.futures
import threading

def upsert(client, project_name, batches):
    
    print("Creating Batches...")

    NUM_BATCHES = len(batches['batches'])

    def upsert_batch(desired_batch, num_retries = 3):
        desired_batch['project'] = project_name
        
        batch_res = client.makeScaleRequest("GET", f"https://api.scale.com/v1/batches/{desired_batch['name']}")

        if (batch_res.status_code == 404):
            print("Batch not found, creating it now...")
    
            batch_creation_res = client.makeScaleRequest("POST", f"https://api.scale.com/v1/batches/", json=desired_batch)
            if (batch_creation_res.status_code != 200):
                print(f"Exiting script, could not create Batch `{desired_batch['name']}`")
                batch_creation_res.raise_for_status()
            else:
                return f"Successfully created batch `{desired_batch['name']}`"

        elif (batch_res.status_code == 200):
            # Batch already exists
            current_batch = batch_res.json()

            # Validate Batch is still in `staging` mode
            if (not batches.get('batchStatusOverride', False) and current_batch['status'] != 'staging'):
                raise(Exception(f"Trying to submit to a non-staging batch, `{desired_batch['name']}` is in status `{current_batch['status']}` | Exiting now"))

            return f"Batch `{desired_batch['name']}` already exists"

        else:
            # Try again if retry > 0
            if (num_retries > 0):
                print(f"Batch creation for `{desired_batch['name']}` failed with status code {batch_res.status_code}, trying {num_retries-1} more times")
                upsert_batch(desired_batch, num_retries-1)
            else: 
                raise(Exception(f"Exiting script, batch creation for {desired_batch['name']} failed"))

    counter = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=client.concurrency_limit) as executor:
        for output in executor.map(upsert_batch, batches['batches']):
            counter += 1
            print(f"{'{:6d}'.format(counter)}/{NUM_BATCHES} | {output}")

def finalize(client, batches):
    print("Finalizing Batches...")

    NUM_BATCHES = len(batches['batches'])

    def finalize_batch(desired_batch, num_retries = 3):

        # See if this batch was already finalized (finalizing again gives bad request)
        batch_res = client.makeScaleRequest("GET", f"https://api.scale.com/v1/batches/{desired_batch['name']}")

        if (batch_res.status_code == 200 and batch_res.json()['status'] == 'in_progress'):
            return f"Batch `{desired_batch['name']}` was already finalized"

        # Need to try and finalize the batch
        batch_finalization_res = client.makeScaleRequest("POST", f"https://api.scale.com/v1/batches/{desired_batch['name']}/finalize")
        # See if we were successful
        if (batch_finalization_res.status_code == 200):
            return f"Batch `{desired_batch['name']}` has been finalized"
        else:
            # Try again if retry > 0
            if (num_retries > 0):
                print(f"Batch creation for `{desired_batch['name']}` failed with status code {batch_finalization_res.status_code}, trying {num_retries-1} more times")
                finalize_batch(desired_batch, num_retries-1)
            else: 
                raise(Exception(f"Exiting script, batch creation for {desired_batch['name']} failed"))

    counter = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=client.concurrency_limit) as executor:
        for output in executor.map(finalize_batch, batches['batches']):
            counter += 1
            print(f"{'{:6d}'.format(counter)}/{NUM_BATCHES} | {output}")