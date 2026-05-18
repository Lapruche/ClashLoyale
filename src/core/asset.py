import logging
from pathlib import Path

import pygame

import constant
from utils import log

__images: dict[str, pygame.Surface] = {}
__fonts: dict[str, pygame.font.Font] = {}
__sounds: dict[str, pygame.mixer.Sound] = {}


# Image
def get_image(path: Path) -> pygame.Surface:
    """
    Stores the image to memory the first time for re-use.

    Args:
        path (pathlib.Path): The path where the image is stored.

    Returns:
        pygame.Surface: An instance of the image's surface.
    """

    trunc_path = path.stem

    if path not in __images.keys():

        try:
            image = pygame.image.load(path)
        except pygame.error:
            log.logger.send(f"Could not load image {trunc_path} as it was not found.", logging.ERROR)

        log.logger.send(f"Loaded image {trunc_path}", constant.TRACE)
        __images[trunc_path] = image
        return image
    else:
        log.logger.send(f"Retrieved image {trunc_path}", constant.TRACE)
        return __images[trunc_path]


def get_image_stem(stem_path: str) -> pygame.Surface | None:
    """
    Gets the stored image from a given name. 
    Cannot load new images from here, use get_image() with the complete path.

    Args:
        stem_path (str): The path where the image is stored.

    Returns:
        pygame.Surface: An instance of the image's surface.
    """

    if stem_path not in __images.keys():
        log.logger.send(f"Could not find an image for stem {stem_path}.", logging.ERROR)
        return None
    else:
        log.logger.send(f"Retrieved image {stem_path}", constant.TRACE)
        return __images[stem_path]


def clear_image(path: Path) -> bool:
    """
    Clears the image from memory if found. 
    Use this if you are sure you won't need it anymore to decrease memory usage.

    Args:
        path (pathlib.Path): The path where the image is stored.

    Returns:
        bool: Whether it was found and deleted or not.
    """

    try:
        del __images[path.stem]
        return True
    except KeyError:
        return False


# Font
def get_font(path: Path, size: int) -> pygame.font.Font:
    """
    Stores the font to memory the first time for re-use.

    Args:
        path (pathlib.Path): The path where the font is stored.
        size (int): The size the font will have.

    Returns:
        pygame.font.Font: An instance of the font.
    """

    trunc_path = path.stem
    index = f"{path}{size}"

    if path not in __fonts.keys():
        try:
            font = pygame.font.Font(path, size)
        except pygame.error:
            log.logger.send(f"Could not load font {path} as it was not found.", logging.ERROR)

        log.logger.send(f"Loaded font {trunc_path} of size {size}", constant.TRACE)
        __fonts[index] = font
        return font
    else:
        log.logger.send(f"Retrieved font {trunc_path}", logging.DEBUG)
        return __fonts[index]


def clear_font(path: Path, size: int) -> bool:
    """
    Clears the font from memory if found.
    Use this if you are sure you won't need it anymore to decrease memory usage.
    
    Args:
        path (pathlib.Path): The path where the font is stored.
        size (int): The size the font has.

    Returns:
        bool: Whether the font was found and deleted or not.
    """

    try:
        del __fonts[f"{path.stem}{size}"]
        return True
    except KeyError:
        return False


# Sound
def get_sound(path: Path) -> pygame.mixer.Sound:
    """
    Stores the sound to memory the first time for re-use.

    Args:
        path (pathlib.Path): The path where the sound is stored.

    Returns:
        pygame.mixer.Sound: An instance of the sound.
    """

    trunc_path = path.stem

    if path not in __sounds.keys():
        try:
            sound = pygame.mixer.Sound(path)
        except pygame.error:
            log.logger.send(f"Could not load sound {trunc_path} as it was not found.", logging.ERROR)

        log.logger.send(f"Loaded sound {trunc_path}", constant.TRACE)
        __sounds[trunc_path] = sound
        return sound
    else:
        log.logger.send(f"Retrieved sound {trunc_path}", constant.TRACE)
        return __sounds[trunc_path]


def clear_sound(path: Path) -> bool:
    """
    Clears the sound from memory if found.
    Use this if you are sure you won't need it anymore to decrease memory usage.

    Args:
        path (pathlib.Path): The path where the sound is stored.

    Returns:
        bool: Whether the sound was found and deleted or not.
    """

    try:
        del __sounds[path.stem]
        return True
    except KeyError:
        return False

# reference: https://www.pygame.org/pcr/caching_resource/index.php
