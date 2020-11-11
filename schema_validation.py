def validate_schema(schema):
    if ("project" not in schema):
        raise(Exception("A Project object needs to be specified | Exiting script, schema Validation Failed"))

    if ("name" not in schema['project']):
        raise(Exception("A Project must have a name | Exiting script, schema Validation Failed"))

    if ("type" not in schema['project']):
        raise(Exception("A Project must have a type | Exiting script, schema Validation Failed"))

    if ('batches' in schema):
        if ('batches' not in schema['batches'] or not isinstance(schema['batches']['batches'], list)):
            raise(Exception("Batches must have an array of batches inside of it | Exiting script, schema Validation Failed"))

    print("Schema has been validated")