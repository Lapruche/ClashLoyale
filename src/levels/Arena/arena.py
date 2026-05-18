from typing import Any, Collection

import pygame

from constant import GUI_PATH, SCREEN_HEIGHT, SCREEN_WIDTH, SPRITES_PATH, TRACE
from core import asset
from levels.Arena.arena_renderer import draw_player_bars, draw_decks, draw_elixir_bars, taunt
from levels.scene import Scene
from managers import player_manager
from utils import log
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

        test_red = ['tasty_crousty', 'x_bow', 'knight', 'pekka', 'prince', 'sapeur', 'zap', 'zappy']
        test_blue = ['canon', 'mini_pekka', 'rage', 'fireball', 'dart_goblin', 'giant', 'hogrider', 'log']

        self.red_plr = player_manager.add_player("rouge", test_red, 3)
        self.blue_plr = player_manager.add_player("bleu", test_blue, 3)

        cards = set(self.blue_plr.deck + self.red_plr.deck)  # Aggregation of both decks to load and scale all images
        self.card_images = load_card_images(cards)

        self.sound.clear_sounds()
        self.sound.play_sound("combat.mp3", 0.75, 2500, True)
        
        # Game actions are temporarily bound here.
        self.input.bind_action("player_1", pygame.K_SPACE, lambda: self.blue_plr.play_card(self.sound, 0))
        self.input.bind_action("player_2", pygame.K_RSHIFT, lambda: self.red_plr.play_card(self.sound, 0))

        # Taunt
        self.input.bind_action("player_1", pygame.K_e, lambda: taunt(self.ui.screen, self.sound, "bleu"))
        self.input.bind_action("player_2", pygame.K_EXCLAIM, lambda: taunt(self.ui.screen, self.sound, "rouge"))

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
