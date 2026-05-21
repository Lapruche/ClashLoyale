# Shared drawing utils here
import pygame

import constant


def scale_by_screen(surface, x_div_scale, y_div_scale):
    return pygame.transform.scale(surface, (constant.SCREEN_WIDTH / x_div_scale, constant.SCREEN_HEIGHT / y_div_scale))


def scale_by_size(surface, scale_factor: tuple):
    size = surface.get_size()
    return pygame.transform.scale(surface, (size[0] * scale_factor[0], size[1] * scale_factor[1]))
