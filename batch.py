def upsert(client, project_name, batches):

    print("\nCreating Batches...")

    def upsert_batch(desired_batch, num_retries=3):
        desired_batch['project'] = project_name

        batch_res = client.get_batch(desired_batch['name'])

        if (batch_res.status_code == 404):
            batch_creation_res = client.create_batch(desired_batch)
            if (batch_creation_res.status_code != 200):
                print(
                    f"❌ Exiting script, could not create Batch `{desired_batch['name']}`")
                batch_creation_res.raise_for_status()
            else:
                return f"✅ Successfully created batch `{desired_batch['name']}`"

        elif (batch_res.status_code == 200):
            # Batch already exists
            current_batch = batch_res.json()

            # Validate Batch is still in `staging` mode
            if (not batches.get('batchStatusOverride', False) and current_batch['status'] != 'staging'):
                raise(Exception(
                    f"❌ Trying to submit to a non-staging batch, `{desired_batch['name']}` is in status `{current_batch['status']}` | Exiting now"))

            return f"✅ Batch '{desired_batch['name']}' already exists, skipping"

        else:
            return f"❌ Batch creation for '{desired_batch['name']}' failed with response {batch_res.json()}"

            # TODO: Same as Task, return error resposne from Scale so the user can fix the payload instad of retrying
            #
            # # Try again if retry > 0
            # if (num_retries > 0):
            #     print(
            #         f"Batch creation for `{desired_batch['name']}` failed with status code {batch_res.status_code}, trying {num_retries-1} more times")
            #     upsert_batch(desired_batch, num_retries-1)
            # else:
            #     raise(Exception(
            #         f"Exiting script, batch creation for {desired_batch['name']} failed"))

    client.execute(upsert_batch, batches['batches'])


def finalize(client, batches):
    print("\nFinalizing Batches...")

    def finalize_batch(batch, num_retries=3):

        batch_name = batch["name"]

        # See if this batch was already finalized (finalizing again gives bad request)
        with client.get_batch(batch_name) as res:
            if (res.status_code == 200 and res.json()['status'] == 'in_progress'):
                return f"✅ Batch '{batch_name}' was already finalized"

        # Try and finalize the batch
        with client.finalize_batch(batch_name) as res:

            if (res.status_code == 200):
                return f"✅ Succesfuly finalized batch '{batch_name}'"
            else:
                return f"❌ Attempt to finalize batch '{desired_batch['name']}' failed with response {res.json()}"

                # TODO: Same as Task, return error resposne from Scale so the user can fix the payload instad of retrying
                #
                # Try again if retry > 0
                # if (num_retries > 0):
                #     print(
                #         f"Batch creation for `{batch_name}` failed with status code {batch_finalization_res.status_code}, trying {num_retries-1} more times")
                #     finalize_batch(desired_batch, num_retries-1)
                # else:
                #     raise(Exception(
                #         f"Exiting script, batch creation for {batch_name} failed"))

    client.execute(finalize_batch, batches['batches'])
