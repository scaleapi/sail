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
