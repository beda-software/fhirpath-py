import os
import json 

model_path = os.path.dirname(__file__)

resources = {}

def save_to_resources(resources, resource_filename):
    filepath = os.path.join(model_path, resource_filename)
    with open(filepath, "r") as paths_file:
        resources[resource_filename] = json.loads(paths_file.read())


save_to_resources(resources, 'observation-example.json')
save_to_resources(resources, 'patient-example.json')
save_to_resources(resources, 'quantity-example.json')
save_to_resources(resources, 'questionnaire-example.json')
save_to_resources(resources, 'valueset-example-expansion.json')