from helpers.concurrency import execute
from scaleapi import exceptions


def upsert(client, project_name, batches):

    print("\n\nCreating Batches...")
    print("===================")

    def upsert_batch(desired_batch):
        batch_name = desired_batch['name']
        batch_callback_url = desired_batch['callback_url']

        try:
            current_batch = client.get_batch(desired_batch['name'])

            # Batch already exists - validate is still in "staging" mode
            if (not batches.get('batchStatusOverride', False) and current_batch.status != 'staging'):
                raise(Exception(
                    f"❌ Trying to submit to a non-staging batch, '{desired_batch['name']}' is in status '{current_batch.status}' | Exiting now"))

            return f"✅ Batch '{desired_batch['name']}' already exists, skipping"

        except exceptions.ScaleResourceNotFound as err:
            try:
                new_batch = client.create_batch(
                    project_name, batch_name, batch_callback_url)
                return f"✅ Successfully created batch `{desired_batch['name']}`"
            except exceptions.ScaleException as err:
                return f"❌ Batch creation for '{desired_batch['name']}' failed <Status Code {err.code}: {err.message}>"

        except exceptions.ScaleException as err:
            return f"❌ Batch fetch for '{desired_batch['name']}' failed <Status Code {err.code}: {err.message}>"

    execute(upsert_batch, batches['batches'])


def finalize(client, batches):
    print("\n\nFinalizing Batches...")
    print("=====================")

    def finalize_batch(batch):

        batch_name = batch["name"]

        # See if this batch was already finalized (finalizing again gives bad request)
        try:
            batch = client.get_batch(batch_name)
            if (batch.status == 'in_progress'):
                return f"✅ Batch '{batch_name}' was already finalized, skipping"

            batch.finalize()
            return f"✅ Succesfuly finalized batch '{batch_name}'"

        except exceptions.ScaleException as err:
            return f"❌ Attempt to finalize batch '{desired_batch['name']}' failed <Status Code {err.code}: {err.message}>"

    execute(finalize_batch, batches['batches'])
