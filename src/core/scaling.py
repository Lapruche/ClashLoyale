import pygame

import constant
from utils import log


def auto_scaling():
    """
    Returns a scaling factor or adapted resolution based on screen size.
    """

    info = pygame.display.Info()
    screen_w, screen_h = info.current_w, info.current_h

    base_w = constant.SCREEN_WIDTH
    base_h = constant.SCREEN_HEIGHT

    log.logger.send(f"Size of the window {screen_w}x{screen_h}", constant.TRACE)

    scale_w = screen_w / base_w
    scale_h = screen_h / base_h

    scale = min(scale_w, scale_h)

    if scale < 1:
        new_w = int(base_w * scale)
        new_h = int(base_h * scale)
        return new_w, new_h

    return base_w, base_h
