import json
import os

import helpers.config as config

def Serialize(data: dict):
    with open (config.PATH_CONFIGURATION, "w", encoding="utf-8") as f:
        f.write(json.dumps(data, indent=4))


def Deserialize():
    data = dict()
    if not os.path.exists(config.PATH_CONFIGURATION):
        return None
    with open (config.PATH_CONFIGURATION, "r", encoding="utf-8") as f:
        data = json.load(f)
        data = data
    return data