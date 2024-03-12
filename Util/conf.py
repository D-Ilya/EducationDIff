import os
import pathlib
import yaml
import re
import json

path_priority = [
    pathlib.Path(__file__).parent.parent / 'conf'
]


class FileTypes:
    YAML = 'yaml'
    JSON = 'json'
    CONF = 'conf'


_read_methods = {
    FileTypes.YAML: yaml.safe_load,
    FileTypes.JSON: json.load
}


def get_config(config_name: str):
    config_path = None
    for base_path in path_priority:
        if os.path.exists(file_path := base_path / config_name):
            config_path = file_path

    if not config_path:
        return

    if file_type := re.search(r"\.(\w+)", config_name):
        file_type = file_type.group(1).lower()
    with open(config_path) as file:
        if func := _read_methods.get(file_type):
            return func(file)
        print()
        return file.read()
