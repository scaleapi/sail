import json


def upsert(client, desired_project):

    print("\n\nCreating Project...")
    print("===================")

    projectParams = desired_project.copy()
    projectParams.pop('name', None)
    projectParams.pop('type', None)

    current_project = None

    # Fetch this project
    project_res = client.get_project(desired_project['name'])

    if (project_res.status_code == 404):
        print("✅ Project not found, creating it now...")

        project_json = {
            "name": desired_project['name'],
            "type": desired_project['type'],
            "params": projectParams
        }

        prj_creation_res = client.create_project(project_json)

        if (prj_creation_res.status_code != 200):
            print("❌ Could not create Project, exiting script")
            prj_creation_res.raise_for_status()
        else:
            # A bit hacky but garaunteed to be true
            print(
                f"✅ Successfully created project '{desired_project['name']}' with version 0"
            )

    elif (project_res.status_code == 200):
        current_project = project_res.json()

        # Check Project Keys
        # First check the type, it's a special one that can't be updated
        if (current_project['type'] != desired_project['type']):
            print(
                f"Project Schema has type '{desired_project['type']}' but this project has type '{current_project['type']}' - Project Types cannot be updated")
            raise(Exception("❌ Project Version Mismatch, exiting script"))

        # Second, most of our project details will sit in the `paramHistory`, let's check our schema keys against what's in the latest param history
        projectNeedsUpdate = False
        latestParamHistory = current_project['param_history'][-1]
        for key in filter(lambda key: key not in ['name', 'type'], desired_project.keys()):
            if not (key in latestParamHistory and latestParamHistory[key] == desired_project[key]):
                print(f"\n❕ Difference in project detected for key '{key}'")
                print("Desired:")
                print(json.dumps(
                    desired_project[key], sort_keys=True, indent=2))
                print("")
                print("Existing:")
                print(json.dumps(latestParamHistory.get(
                    key, '<Not Specified>'), sort_keys=True, indent=2))
                projectNeedsUpdate = True

        if (projectNeedsUpdate):
            # Create a new project version
            param_history_res = client.request(
                "POST", f"https://api.scale.com/v1/projects/{desired_project['name']}/setParams", json=projectParams)
            if (param_history_res.status_code != 200):
                raise(Exception(
                    f"❌ Error {param_history_res.status_code} | Exiting script, Could not update Project"))
            else:
                # A bit hacky but garaunteed to be true
                log(
                    f"✅ Successfully updated project to version {len(current_project['param_history'])}")
        else:
            log(
                f"✅ Project '{desired_project['name']}' found with matching schema, skipping")
    else:
        raise(Exception(f"❌ Error retreiving project {project_res.json()}\n"))


def log(string):
    print(f"{'{:11s}'.format('')}{string}")
