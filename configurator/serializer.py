import json
import os

import helpers.config as config

def Serialize(data: dict):
    if not os.path.exists(config.PATH_USERCONFIG):
        os.mkdir(config.PATH_USERCONFIG)
    with open (f"{config.PATH_USERCONFIG}{os.sep}{config.FILE_USERCONFIG}", "w", encoding="utf-8") as f:
        f.write(json.dumps(data))


def Deserialize():
    data = dict()
    if not os.path.exists(config.PATH_USERCONFIG):
        return None
    with open (f"{config.PATH_USERCONFIG}{os.sep}{config.FILE_USERCONFIG}", "r", encoding="utf-8") as f:
        data = json.load(f)
        data = data
    return data