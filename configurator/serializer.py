import json
import os

import helpers.config as config

def Serialize(data: dict):
    with open (f"{config.PATH_ROOT}{os.sep}{config.FILENAME_CONFIGURATION}", "w", encoding="utf-8") as f:
        f.write(json.dumps(data, indent=4))


def Deserialize():
    data = dict()
    if not os.path.exists(f"{config.PATH_ROOT}{os.sep}{config.FILENAME_CONFIGURATION}"):
        return None
    with open (f"{config.PATH_ROOT}{os.sep}{config.FILENAME_CONFIGURATION}", "r", encoding="utf-8") as f:
        data = json.load(f)
        data = data
    return data