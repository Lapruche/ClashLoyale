import pygame

from constant import BLUE_COLOR, RED_COLOR, SCREEN_WIDTH, SCREEN_HEIGHT, ELIXIR_COLOR, GUI_SOUNDS_PATH
from core.sound import Sound
from core.ui import UI
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


def draw_elixir_bars(ui_module: UI, elixir_bar, blue_x, red_x, y_offset):
    screen = ui_module.screen
    blue_elixir = player_manager.get_player("bleu").elixir
    red_elixir = player_manager.get_player("rouge").elixir

    bar_size = elixir_bar.get_size()

    pygame.draw.rect(ui_module.screen, ELIXIR_COLOR,
                     pygame.Rect(blue_x, y_offset, bar_size[0], bar_size[1] / 10 * blue_elixir))
    pygame.draw.rect(ui_module.screen, ELIXIR_COLOR,
                     pygame.Rect(red_x, y_offset, bar_size[0], bar_size[1] / 10 * red_elixir))

    blue_text = ui_module.font_small.render(str(blue_elixir), True, BLUE_COLOR)
    red_text = ui_module.font_small.render(str(red_elixir), True, RED_COLOR)

    screen.blit(blue_text, (blue_x, y_offset - 50))
    screen.blit(red_text, (red_x, y_offset - 50))
    screen.blit(elixir_bar, (blue_x, y_offset))  # Blue elixir bar
    screen.blit(elixir_bar, (red_x, y_offset))  # Red elixir bar


def taunt(screen, sound_module: Sound, camp):
    sound_module.play_sound(GUI_SOUNDS_PATH / "taunt.wav", 0.4)
    # TODO: taunt blit
