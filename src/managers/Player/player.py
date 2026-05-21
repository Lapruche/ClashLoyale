import logging
from random import shuffle

from constant import TRACE, GUI_SOUNDS_PATH
from core.sound import Sound
from managers.cursor_manager import Cursor
from utils import log


class Player:
    def __init__(self, keymap_context: str, cursor: Cursor, camp: str, deck: list, elixir_start: int) -> None:
        self.keymap_context = keymap_context
        self.cursor = cursor
        self.camp = camp
        self.deck = deck  # 8 Cards
        self.elixir = elixir_start  # 0 - 10

        self.hand = []  # Playable cards
        self.draw_pile = []  # Cards to cycle

    def modify_elixir(self, amount: int) -> None:
        self.elixir = max(0, min(10, self.elixir + amount))
        log.logger.send(f"Modified elixir for player {self.camp} to {self.elixir}.", TRACE)

    def populate_deck(self) -> None:
        game_deck = self.deck.copy()

        shuffle(game_deck)

        self.hand = game_deck[:4]
        self.draw_pile = game_deck[4:]

    def play_card(self, sound_module: Sound, index: int) -> None:
        card = self.hand[index]
        next_card = self.draw_pile.pop(0)

        self.hand[index] = next_card
        self.draw_pile.append(card)

        sound_module.play_sound(GUI_SOUNDS_PATH / "elixir.wav", 0.3)

        log.logger.send(f"Player {self.camp} plays card {card}.", logging.DEBUG)
