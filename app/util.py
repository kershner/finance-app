import json
import os


def get_parameters():
    # Load params from JSON file
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    with open(base_dir + '/parameters.json') as f:
        params = json.load(f)
        return params
