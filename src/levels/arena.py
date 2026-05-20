import pygame

from constant import BLUE_COLOR, ELIXIR_COLOR, GUI_PATH, RED_COLOR, SCREEN_HEIGHT, SCREEN_WIDTH, SPRITES_PATH
from core import asset
from levels.scene import Scene
from managers import player_manager, round_manager


def draw_player_bars(screen, bar_width):
    pygame.draw.rect(screen, BLUE_COLOR, pygame.Rect(0, 0, bar_width, SCREEN_HEIGHT))
    pygame.draw.rect(screen, RED_COLOR, pygame.Rect(SCREEN_WIDTH - bar_width, 0, bar_width, SCREEN_HEIGHT))


def draw_decks(screen, blue_deck, red_deck, start_y, y_offset):
    y = start_y

    for i in range(4):
        card_blue = blue_deck[i]
        card_red = red_deck[i]

        screen.blit(card_blue, (50, y))
        screen.blit(card_red, (SCREEN_HEIGHT - 175, y))

        y += y_offset


def draw_elixir_bars(screen, elixir_bar, blue_x, red_x, y_offset):
    blue_elixir = player_manager.get_player("bleu").elixir
    red_elixir = player_manager.get_player("rouge").elixir

    bar_size = elixir_bar.get_size()

    pygame.draw.rect(screen, ELIXIR_COLOR, pygame.Rect(blue_x, y_offset, bar_size[0], bar_size[1] / 10 * blue_elixir))
    pygame.draw.rect(screen, ELIXIR_COLOR, pygame.Rect(red_x, y_offset, bar_size[0], bar_size[1] / 10 * red_elixir))

    screen.blit(elixir_bar, (blue_x, y_offset))  # Blue elixir bar
    screen.blit(elixir_bar, (red_x, y_offset))  # Red elixir bar   


class Arena(Scene):
    def __init__(self, modules: dict):
        super().__init__(modules)  # Initializes the scene

        self.modules = modules
        self.state_manager = modules["state"]
        self.input = modules["input"]
        self.ui = modules["ui"]
        self.sound = modules["sound"]

        self.arena = asset.get_image(SPRITES_PATH / "arena.png")
        self.arena_size = self.arena.get_size()
        self.arena_ratio = SCREEN_HEIGHT / self.arena_size[1]
        self.arena = pygame.transform.scale(self.arena, (int(self.arena_size[0] * self.arena_ratio), SCREEN_HEIGHT))
        self.arena_size = self.arena.get_size()  # Gets new scaled size.
        self.arena_pos = (SCREEN_WIDTH / 2 - self.arena_size[0] / 2, 0)

        self.elixir_bar = asset.get_image(GUI_PATH / "elixir_bar.png")
        self.elixir_bar_size = self.elixir_bar.get_size()

        self.blue_plr = None
        self.red_plr = None

    def start(self):
        super().start()
        round_manager.add_round(175)

        test_red = ['tasty_crousty', 'x_bow', 'knight', 'pekka', 'prince', 'sapeur', 'zap', 'zappy']
        test_blue = ['canon', 'mini_pekka', 'rage', 'fireball', 'dart_goblin', 'giant', 'hogrider', 'log']

        self.red_plr = player_manager.add_player("rouge", test_red, 3)
        self.blue_plr = player_manager.add_player("bleu", test_blue, 3)

        bar_width = 15

        self.sound.clear_sounds()
        self.sound.play_sound("combat.mp3", 2500, True)

    def run(self):
        super().run()

        self.ui.screen.blit(self.arena, self.arena_pos)
        draw_player_bars(self.ui.screen, 15)
        draw_decks(self.ui.screen, self.blue_plr.deck_img, self.red_plr.deck_img, 150, 175)
        draw_elixir_bars(self.ui.screen,
                         self.elixir_bar,
                         SCREEN_WIDTH / 2 - self.arena_size[0] / 2 - 40,
                         SCREEN_WIDTH / 2 + self.arena_size[0] / 2 + 20,
                         SCREEN_HEIGHT / 2 - self.elixir_bar_size[1] / 2
                         )
