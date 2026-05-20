from typing import Any, Collection

import pygame

from constant import GUI_PATH, SCREEN_HEIGHT, SCREEN_WIDTH, SPRITES_PATH, TRACE
from core import asset
from levels.Arena.arena_renderer import draw_player_bars, draw_decks, draw_elixir_bars
from levels.Arena.card_placement import CardPlacementHandler
from levels.scene import Scene
from managers import player_manager, cursor_manager
from utils import log
from utils.binding_states import bind_default_actions
from utils.log import Logger
from utils.scale_card import scale_card


def load_card_images(cards: Collection[str]) -> dict[Any, Any]:
    images = {}

    for card in cards:
        card_img = asset.get_image_stem(card)
        if card_img:
            images[card] = scale_card(card_img, 8, 6.5)

    log.logger.send(f"Loaded and scaled {len(cards)} card images.", TRACE)
    return images


class Arena(Scene):
    def __init__(self, modules: dict) -> None:
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
        self.card_images = None

    def start(self) -> None:
        super().start()
        
        log.logger.send("Game started.")

        test_red = ['tasty_crousty', 'x_bow', 'knight', 'pekka', 'prince', 'sapeur', 'zap', 'zappy']
        test_blue = ['canon', 'mini_pekka', 'rage', 'fireball', 'dart_goblin', 'giant', 'hogrider', 'log']

        cursor_manager.init_arena_cursors()
        blue_cursor = cursor_manager.get_cursor("bleu")
        red_cursor = cursor_manager.get_cursor("rouge")

        self.blue_plr = player_manager.add_player("player_1", blue_cursor, "bleu", test_blue, 3)
        self.red_plr = player_manager.add_player("player_2", red_cursor, "rouge", test_red, 3)

        cards = set(self.blue_plr.deck + self.red_plr.deck)  # Aggregation of both decks to load and scale all images
        self.card_images = load_card_images(cards)

        self.sound.clear_sounds()
        self.sound.play_sound("combat.mp3", 0.75, 2500, True)

        card_placement = CardPlacementHandler(self.modules)
        bind_default_actions(self.red_plr, self.modules)
        bind_default_actions(self.blue_plr, self.modules)

    def run(self) -> None:
        super().run()

        self.ui.screen.blit(self.arena, self.arena_pos)
        draw_player_bars(self.ui.screen, 15)
        draw_decks(self.ui.screen, self.blue_plr, self.red_plr, self.card_images, 150, 175)
        draw_elixir_bars(self.ui,
                         self.elixir_bar,
                         SCREEN_WIDTH / 2 - self.arena_size[0] / 2 - 40,
                         SCREEN_WIDTH / 2 + self.arena_size[0] / 2 + 20,
                         SCREEN_HEIGHT / 2 - self.elixir_bar_size[1] / 2
                         )
