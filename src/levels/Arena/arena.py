from typing import Any, Collection

import pygame

from constant import GUI_PATH, SCREEN_HEIGHT, SCREEN_WIDTH, SPRITES_PATH, TRACE, START_ELIXIR
from core import asset
from levels.Arena.arena_renderer import draw_player_bars, draw_decks, draw_elixir_bars, draw_cursors, draw_timer
from levels.scene import Scene
from managers import cursor_manager, round_manager
from managers.Player import player_manager
from managers.Unit.unit_manager import UnitManager
from utils import log
from utils.binding_states import BindingsHelper
from utils.drawing import scale_by_screen


def load_card_images(cards: Collection[str]) -> dict[Any, Any]:
    images = {}

    for card in cards:
        card_img = asset.get_image_stem(card)
        if card_img:
            images[card] = scale_by_screen(card_img, 8, 6.5)

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

        self.blue_cursor = scale_by_screen(asset.get_image(GUI_PATH / "blue_cursor.png"), 30, 30)
        self.red_cursor = scale_by_screen(asset.get_image(GUI_PATH / "red_cursor.png"), 30, 30)

        self.unit_manager = UnitManager(self.modules, (0, 0))
        self.unit_manager.init_hpbar_sprites()

        self.blue_plr = None
        self.red_plr = None
        self.card_images = None

    def start(self) -> None:
        super().start()
        round_manager.add_round(175)

        test_red = ['tasty_crousty', 'x_bow', 'knight', 'pekka', 'prince', 'wall_breaker', 'zap', 'zappy']
        test_blue = ['canon', 'mini_pekka', 'rage', 'fireball', 'dart_goblin', 'giant', 'hog_rider', 'log']
        test_knight = ['knight', 'knight', 'knight', 'knight', 'knight', 'knight', 'knight', 'knight']

        cursor_manager.init_arena_cursors()
        bindings_helper = BindingsHelper(self.modules, self.unit_manager)

        # Setup player cursors
        blue_cursor = cursor_manager.get_cursor("bleu")
        red_cursor = cursor_manager.get_cursor("rouge")

        if blue_cursor is None or red_cursor is None:
            raise AttributeError("Could not get player cursors, something went very wrong !")

        # Setup players
        self.blue_plr = player_manager.add_player("player_1", blue_cursor, "bleu", test_knight, START_ELIXIR)
        self.red_plr = player_manager.add_player("player_2", red_cursor, "rouge", test_knight, START_ELIXIR)

        if self.blue_plr is None or self.red_plr is None:
            raise AttributeError("Could not add players, something went very wrong !")

        # Loads and scales images from both decks
        cards = set(self.blue_plr.deck + self.red_plr.deck)
        self.card_images = load_card_images(cards)

        self.sound.clear_sounds()  # Prevents overlapping soundtracks
        self.sound.play_sound("combat.mp3", 0.5, 2500, True)

        # Binds player inputs
        bindings_helper.bind_ingame_actions(self.blue_plr)
        bindings_helper.bind_ingame_actions(self.red_plr)

        log.logger.send("Game started.")

        # Spawn towers
        self.unit_manager.spawn_unit("king_tower", "bleu", (500, 915))
        self.unit_manager.spawn_unit("king_tower", "rouge", (500, 125))

        self.unit_manager.spawn_unit("princess_tower", "bleu", (340, 860))  # Left
        self.unit_manager.spawn_unit("princess_tower", "bleu", (660, 860))  # Right

        self.unit_manager.spawn_unit("princess_tower", "rouge", (340, 175))  # Left
        self.unit_manager.spawn_unit("princess_tower", "rouge", (660, 175))  # Right

    def run(self, dt=0) -> None:
        super().run(dt)
        self.unit_manager.tick(dt)

        player_deck_indexes = (self.blue_plr.cursor.card_index, self.red_plr.cursor.card_index)

        self.ui.screen.blit(self.arena, self.arena_pos)

        draw_player_bars(self.ui.screen, 15)
        draw_decks(self.ui.screen, self.blue_plr, self.red_plr, self.card_images, player_deck_indexes, 150, 175)
        draw_timer(self.ui)
        draw_elixir_bars(self.ui,
                         self.elixir_bar,
                         SCREEN_WIDTH / 2 - self.arena_size[0] / 2 - 40,
                         SCREEN_WIDTH / 2 + self.arena_size[0] / 2 + 20,
                         SCREEN_HEIGHT / 2 - self.elixir_bar_size[1] / 2
                         )

        self.unit_manager.draw(self.ui.screen)

        draw_cursors(self.ui.screen, (self.blue_cursor, self.red_cursor), (self.blue_plr.cursor, self.red_plr.cursor))
