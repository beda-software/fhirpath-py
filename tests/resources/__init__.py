import json
import os
import pathlib

current_dir = pathlib.Path(__file__).parent.resolve()

resources = {}


files = [f for f in os.listdir(current_dir)]
for f in files:
    fp = os.path.join(current_dir, f)
    print(fp)
    if os.path.isfile(fp) and f.endswith(".json"):
        with open(fp) as fd:
            resources[f] = json.loads(fd.read())
