import json
import os
from argparse import ArgumentParser
from helpers import schema_validation
from helpers.client import Sail
from models import project, batch, task
from example_schemas.schema_with_batches import schema


def main():
    # Specify your API Key, test_xxxx or live_xxxx
    if 'API_KEY' not in os.environ:
        raise(Exception(f"❌ Missing API_KEY as environment variable\n"))

    # Load args
    args = get_args()
    finalize_batches = args.finalize_batches

    # Create a Sail client to handle making requests to Scale
    client = Sail(os.environ["API_KEY"])

    # Validate the schema
    schema_validation.validate(schema)

    # Get or Create the Project
    project.upsert(client, schema['project'])

    # If we're using batches, create them
    if ('batches' in schema):
        batch.upsert(client, schema['project']['name'], schema['batches'])

    # Create all tasks specified in schema
    task.create(client, schema['project'], schema.get(
        'batches', None), schema['tasks'])

    # If we were using batches and --finalize-batches flag is present, do so
    if ('batches' in schema and finalize_batches):
        batch.finalize(client, schema['batches'])


def get_args():
    ap = ArgumentParser()
    ap.add_argument('--finalize-batches', action='store_true')
    return ap.parse_args()


if __name__ == "__main__":
    print("")
    main()
    print("\n")


# TODOS:
# Add Timeout + Try/Catch to Requests
# Add Timers (Start/Stop) to batches and task creation
