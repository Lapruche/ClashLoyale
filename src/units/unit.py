import json
import logging
import os

import constant
from constant import DEFINITIONS_PATH
from utils import log


class Unit:
    def __init__(self, name):
        self.name = name
        self.file = ""

        list_files = os.listdir(DEFINITIONS_PATH)

        for file in list_files:
            if file.startswith(str(self.name)):
                self.file = file

        if len(self.file) == 0:
            log.logger.send(f"Could not load unit {self.name}, file not found.", logging.ERROR)
            return
        else:
            log.logger.send(f"Registered unit {self.name}.", constant.TRACE)

        self.data = json.load(open(DEFINITIONS_PATH / self.file))
