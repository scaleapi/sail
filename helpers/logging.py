import json


def log_success(string):
    print(f"{'{:11s}'.format('')}✅ {string}")


def log_json(dict):
    print(json.dumps(dict, sort_keys=True, indent=2))
