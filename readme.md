# Scale Sail

Sail is a data pipeline starter kit meant to optimize how you provide data to Scale.

It's meant to have the following included:

- Project level Pipeline Config (with versioning abstracted)
- Batch Creation and Finalization (both Easy and Complex cases)
- Task Creation based on a .csv mapping, .json file, or just a Python Dictionary, longer term goal to support passing in a folder location or S3 bucket URI
- Concurrency for every operation so scripts can run ~30x faster
- Logging built-in
- Error Handling and retries on every part + Idempotency for Task creation

We've done our best to abstract the data pipeline nuances and incorporate Scale best practices throughout

# How to start
- Python 3.6+ is required to run these scripts.
- `API_KEY` environment variable must be set.
- Modify files under `example_schema`.
- Run the main sail script `API_KEY=live_xxx python sail.py`.

# Schema
Runing `sail.py` will create a project with batches and tasks.

Detailed info on these entitites can be found on Scale Docs:

- Project: https://docs.scale.com/reference#projects
- Batch: https://docs.scale.com/reference#batches
- Task: https://docs.scale.com/reference#task-object

# Idempotency
There's a highly recommended, yet optional, field called `unique_id`. It will prevent the creation of duplicated tasks.

It can be set at the task level manually. Or, using the flag `generateUniqueId`, all tasks missing the `unique_id` field will generate one in the form of `<project_name>_<batch_name>_<attachment_url>`.

# Recommended workflow
1. Run as many times as necessary, using `unique_id` to ensure no duplicated tasks.
2. After having project, batches and tasks created as desired, run one more time using the `--finalize-batches` flag. 
3. After a batch is finalized, tasks start beeing worked on. 
- Note that new tasks cannot be submitted into a finalized batch.