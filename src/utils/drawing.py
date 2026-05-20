# Shared drawing utils here
import pygame

import constant


def scale_surface(surface, x_div_scale, y_div_scale):
    return pygame.transform.scale(surface, (constant.SCREEN_WIDTH / x_div_scale, constant.SCREEN_HEIGHT / y_div_scale))
