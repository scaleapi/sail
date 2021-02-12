import json
from helpers.logging import log_success


def upsert(client, desired_project):

    print("\n\nCreating Project...")
    print("===================")

    project_name = desired_project['name']

    project_params = desired_project.copy()
    project_params.pop('name', None)
    project_params.pop('type', None)

    current_project = None

    # Fetch this project
    prev_project_res = client.get_project(project_name)

    if (prev_project_res.status_code == 404):
        log_success("Project not found, creating it now...")

        payload = {
            "name": project_name,
            "type": desired_project['type'],
            "params": project_params
        }

        new_project_res = client.create_project(payload)

        if (new_project_res.status_code != 200):
            print("❌ Could not create Project, exiting script")
            new_project_res.raise_for_status()
        else:
            # A bit hacky but garaunteed to be true
            log_success(
                f"Successfully created project '{project_name}' with version 0"
            )

    elif (prev_project_res.status_code == 200):
        current_project = prev_project_res.json()

        # Check Project Keys
        # First check the type, it's a special one that can't be updated
        if (current_project['type'] != desired_project['type']):
            print(
                f"Project Schema has type '{desired_project['type']}' but this project has type '{current_project['type']}' - Project Types cannot be updated")
            raise(Exception("❌ Project Version Mismatch, exiting script"))

        # Second, most of our project details will sit in the `paramHistory`, let's check our schema keys against what's in the latest param history
        project_needs_update = False
        last_params = current_project['param_history'][-1]
        for key in filter(lambda key: key not in ['name', 'type'], desired_project.keys()):
            if not (key in last_params and last_params[key] == desired_project[key]):
                print(f"\n❕ Difference in project detected for key '{key}'")
                print("Desired:")
                print(json.dumps(
                    desired_project[key], sort_keys=True, indent=2))
                print("")
                print("Existing:")
                print(json.dumps(last_params.get(
                    key, '<Not Specified>'), sort_keys=True, indent=2))
                project_needs_update = True

        if (project_needs_update):
            # Create a new project version
            with client.update_project(project_name, project_params) as res:
                if (res.status_code != 200):
                    raise(Exception(
                        f"❌ Update paramas for project '{project_name}'' failed with response {res.json()}"))
                else:
                    # A bit hacky but garaunteed to be true
                    log_success(
                        f"Successfully updated project '{project_name}'' to version {len(current_project['param_history'])}")
        else:
            log_success(
                f"Project '{project_name}' found with matching schema, skipping")
    else:
        raise(
            Exception(f"❌ Error retreiving project {prev_project_res.json()}\n"))
