# Sail

Sail is a data pipeline starter kit meant to optimize how you provide data to Scale.

It's meant to have the following included:

- Project level Pipeline Config (with versioning abstracted)
- Batch Creation and Finalization (both Easy and Complex cases)
- Task Creation based on a .csv mapping, .json file, or just a Python Dictionary. A longer-term goal is to support passing in a folder location or S3 Bucket URI.
- Concurrency for every operation so scripts can run ~30x faster
- Logging built-in
- Error Handling and retries on every part + Idempotency for Task creation

We've done our best to abstract the data pipeline nuances and incorporate Scale best practices throughout

# Getting started
- Python 3.6+ is required to run these scripts.
- `API_KEY` environment variable must be set.
- Modify `example_schemas/schema.py`. It's an example Python dictionary describing the project and tasks to be created. It has comments on what each field is, and more detailed documentation can be found in the [Schema Section](#Schema).
- Run the main Sail script. A __Test API Key__ can be used to try out the API and the platform. When ready to create a production project, just switch to a __Live API Key__:
```
API_KEY=live_xxx python sail.py
```

# Working with batches
For large projects, batches can be created to group tasks between the same project. There's an example schema on `example_schemas/schema_with_batches.py`.

More detailed documentation can be found in the [Schema Section](#Schema)

Also, there's a [recommended workflow](#recommended-workflow) for working with batches.

# Schema
Running `sail.py` will create a project with batches and tasks.

Detailed info on these entities and how Scale works can be found on Scale Docs:

- Scale 101: https://scale.com/docs/key-concepts <- Start Here!
- Project: https://docs.scale.com/reference#projects
- Batch: https://docs.scale.com/reference#batches
- Task: https://docs.scale.com/reference#task-object

# Idempotency
There's a highly recommended, yet optional, field called `unique_id`. It will prevent the creation of duplicated tasks.

It can be set at the task level manually. Or, using the flag `generateUniqueId`, all tasks missing the `unique_id` field will generate one in the form of `<project_name>_<batch_name>_<attachment_url>`.

# Recommended workflow
1. Run as many times as necessary, using `unique_id` to ensure no duplicated tasks.
2. After having the project, batches, and tasks created as desired, run one more time using the `--finalize-batches` flag. 
3. After a batch is finalized, tasks start being worked on. 
- Note that new tasks cannot be submitted into a finalized batch.

# Task download
There is also a script `task_download.py`, which can be used for downloading all tasks from a project. 

There's an optional `--resume` flag that allows resuming on a previous run. It will download only new batches. Also, if when running it for a large project some errors occur, this flag allows re-running the script downloading only the errored batches.

Usage:

```
python task_download.py --api-key live_xxxx --project project_name --resume
```
