import os
import json


# TODO make this thing awesome


def read_json_file(filename):
    """
    File name regarding to roses folder.
    """
    path = get_path(filename)
    with open(path) as f:
        content = json.loads(f.read())
    return content


def get_path(filename):
    base_path = os.path.dirname(os.path.abspath(__file__))
    return "".join([base_path, "/", filename])
