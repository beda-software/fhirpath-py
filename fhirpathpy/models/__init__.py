import json
import os
import pathlib
from collections import defaultdict

current_dir = pathlib.Path(__file__).parent.resolve()

models = defaultdict(dict)

dirs = [f for f in os.listdir(current_dir)]

for d in dirs:
    pd = os.path.join(current_dir, d)
    if os.path.isdir(pd):
        for f in os.listdir(pd):
            with open(os.path.join(pd, f)) as fd:
                if f.endswith(".json"):
                    models[d][f[:-5]] = json.loads(fd.read())
