import logging
from pathlib import Path

from constant import BLUE_SPRITES, RED_SPRITES
from core import asset
from core.animation import Animation
from utils import log


def animation_from_folder_path(folder_path: Path, frame_name: str, frames_duration: float, loop: bool = True):
    frames = []

    for file in sorted(folder_path.glob(f"{frame_name}*.png")):
        frames.append(asset.get_image(folder_path / file).convert_alpha())

    if len(frames) == 0:
        log.logger.send(f"Animation creation failed. Could not find any frames for {folder_path.stem}:{frame_name}",
                        logging.ERROR)
        return None

    return Animation(frames, frames_duration, loop)


def unit_animation(unit_name: str, frame_name: str, camp: str, frames_duration: float, loop: bool = False):
    path = BLUE_SPRITES / unit_name if camp == "bleu" else RED_SPRITES / unit_name
    return animation_from_folder_path(path, frame_name, frames_duration, loop)
