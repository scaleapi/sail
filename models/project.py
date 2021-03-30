import json
from helpers.logging import log_success, log_json
from scaleapi import exceptions
from scaleapi.tasks import TaskType


def upsert(client, desired_project):

    print("\n\nCreating Project...")
    print("===================")

    project_name = desired_project['name']

    project_params = desired_project.copy()
    project_params.pop('name', None)
    project_params.pop('type', None)

    current_project = None

    try:
        # Fetch this project
        current_project = client.get_project(project_name)

        # Check Project Keys
        # First check the type, it's a special one that can't be updated
        if (current_project.type != desired_project['type']):
            raise(Exception(
                f"❌ Project Schema has type '{desired_project['type']}' but this project has type '{current_project.type}' - Project Types cannot be updated"))

        # Second, most of our project details will sit in the `paramHistory`, let's check our schema keys against what's in the latest param history
        project_needs_update = False
        last_params = current_project.last_params
        for key in filter(lambda key: key not in ['name', 'type'], desired_project.keys()):
            if not (key in last_params and last_params[key] == desired_project[key]):
                print(f"\n❕ Difference in project detected for key '{key}'")
                print("\nDesired:")
                log_json(desired_project[key])
                print("\nExisting:")
                log_json(last_params.get(key, '<Not Specified>'))
                project_needs_update = True

        if (project_needs_update):
            # Create a new project version
            try:
                client.update_project(project_name, **project_params)
                log_success(
                    f"Successfully updated project '{project_name}' to version {len(current_project.as_dict()['param_history'])}")
            except exceptions.ScaleException as err:
                raise(Exception(
                    f"❌ Update paramas for project '{project_name}' failed <Status Code {err.code}: {err.message}>"))
                # A bit hacky but garaunteed to be true
        else:
            log_success(
                f"Project '{project_name}' found with matching schema, skipping")

    except exceptions.ScaleResourceNotFound as err:
        log_success("Project not found, creating it now...")
        task_type = TaskType(desired_project['type'])
        try:
            new_project = client.create_project(
                project_name, task_type, project_params)
            log_success(
                f"Successfully created project '{project_name}' with version 0")
        except exceptions.ScaleException as err:
            print(
                f"❌ Project creation for '{project_name}' failed <Status Code {err.code}: {err.message}>")

    except exceptions.ScaleException as err:
        print(
            f"❌ Project fetch for '{project_name}' failed <Status Code {err.code}: {err.message}>")
