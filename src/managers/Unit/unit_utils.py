import json
import logging
import os
from pathlib import Path

import constant
from constant import DEFINITIONS_PATH, BLUE_SPRITES, RED_SPRITES
from core import asset
from utils import log
from utils.drawing import scale_unit


def get_definition(unit_name: str):
    list_files = os.listdir(DEFINITIONS_PATH)

    for file in list_files:
        if file.startswith(unit_name):
            definitions = json.load(open(os.path.join(DEFINITIONS_PATH, file), "r"))
            if definitions is not None:
                log.logger.send(f"Retrieved definitions for unit {unit_name}.", constant.TRACE)
                return definitions

    log.logger.send(f"Could not load unit {unit_name}, file not found.", logging.ERROR)
    return None


def get_sprite(unit_name: str, camp: str, state: str):
    sprites_dir = BLUE_SPRITES if camp == "bleu" else RED_SPRITES
    unit_dir = sprites_dir / unit_name

    if not unit_dir.is_dir():
        log.logger.send(f"Could not load sprite for unit {unit_name}, folder {unit_dir} not found.", logging.ERROR)
        return None

    for file in sorted(os.listdir(unit_dir)):
        stem = Path(file).stem
        if stem.startswith(state) or stem.endswith(state):
            sprite = asset.get_image(unit_dir / file)
            if sprite is not None:
                log.logger.send(f"Retrieved sprite for unit {unit_name}.", constant.TRACE)
                return scale_unit(sprite, 3, 3)
            log.logger.send(f"Could not load sprite for unit {unit_name}.", logging.ERROR)
    return None
