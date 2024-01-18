import os
import json

import pathlib

current_dir = pathlib.Path(__file__).parent.resolve()

resources = {}


def save_to_resources(re, filepath):
    resources[resource_filename] = json.loads(paths_file.read())


files = [f for f in os.listdir(current_dir)]
for f in files:
    fp = os.path.join(current_dir, f)
    print(fp)
    if os.path.isfile(fp) and f.endswith(".json"):
        with open(fp, "r") as fd:
            resources[f] = json.loads(fd.read())
