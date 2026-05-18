import pygame

import constant


def scale_card(card, x_div_scale, y_div_scale):
    return pygame.transform.scale(card, (constant.SCREEN_WIDTH / x_div_scale, constant.SCREEN_HEIGHT / y_div_scale))
