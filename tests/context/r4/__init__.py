import os
import json

model = {}

model_path = os.path.dirname(__file__)
type_paths_filepath = os.path.join(model_path, "choiceTypePaths.json")
defined_paths_filepath = os.path.join(model_path, "pathsDefinedElsewhere.json")

with open(type_paths_filepath, "r") as paths_file:
    model["choiceTypePaths"] = json.loads(paths_file.read())

with open(defined_paths_filepath, "r") as paths_file:
    model["pathsDefinedElsewhere"] = json.loads(paths_file.read())
