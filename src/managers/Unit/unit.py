import json
import logging
import os

import constant
from constant import DEFINITIONS_PATH
from utils import log


def get_definition(unit_name: str):
    list_files = os.listdir(DEFINITIONS_PATH)

    for file in list_files:
        if file.startswith(unit_name):
            log.logger.send(f"Retrieved definitions for unit {unit_name}.", constant.TRACE)
            return json.load(open(file, "r"))

    log.logger.send(f"Could not load unit {unit_name}, file not found.", logging.ERROR)
    return None
