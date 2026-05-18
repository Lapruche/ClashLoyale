import pygame

from constant import BLUE_COLOR, RED_COLOR, SCREEN_WIDTH, SCREEN_HEIGHT, ELIXIR_COLOR
from managers import player_manager


def draw_player_bars(screen, bar_width):
    pygame.draw.rect(screen, BLUE_COLOR, pygame.Rect(0, 0, bar_width, SCREEN_HEIGHT))
    pygame.draw.rect(screen, RED_COLOR, pygame.Rect(SCREEN_WIDTH - bar_width, 0, bar_width, SCREEN_HEIGHT))


def draw_decks(screen, blue_player, red_player, card_images, start_y, y_offset):
    for i in range(4):
        y = start_y + i * y_offset
        blue_card = card_images.get(blue_player.hand[i])
        red_card = card_images.get(red_player.hand[i])

        # BLUE (50,y)
        # RED (SCREEN_WIDTH - 175, y)
        screen.blit(blue_card, (50, y))
        screen.blit(red_card, (SCREEN_WIDTH - 175, y))


def draw_elixir_bars(screen, elixir_bar, blue_x, red_x, y_offset):
    blue_elixir = player_manager.get_player("bleu").elixir
    red_elixir = player_manager.get_player("rouge").elixir

    bar_size = elixir_bar.get_size()

    pygame.draw.rect(screen, ELIXIR_COLOR, pygame.Rect(blue_x, y_offset, bar_size[0], bar_size[1] / 10 * blue_elixir))
    pygame.draw.rect(screen, ELIXIR_COLOR, pygame.Rect(red_x, y_offset, bar_size[0], bar_size[1] / 10 * red_elixir))

    screen.blit(elixir_bar, (blue_x, y_offset))  # Blue elixir bar
    screen.blit(elixir_bar, (red_x, y_offset))  # Red elixir bar
