
import logging
from random import shuffle

from constant import TRACE
from utils import log


class Player:
    def __init__(self, camp, deck, elixir_start) -> None:
        self.camp = camp
        self.deck = deck  # 8 Cards
        self.elixir = elixir_start  # 0 - 10

        self.hand = []  # Playable cards
        self.draw_pile = []  # Cards to cycle

    def modify_elixir(self, amount):
        self.elixir = max(0, min(10, self.elixir + amount))
        log.logger.send(f"Modified elixir for player {self.camp} to {self.elixir}.", TRACE)

    def populate_deck(self):
        game_deck = self.deck.copy()

        shuffle(game_deck)

        self.hand = game_deck[:4]
        self.draw_pile = game_deck[4:]

    def play_card(self, index):
        card = self.hand[index]
        next_card = self.draw_pile.pop(0)

        self.hand[index] = next_card
        self.draw_pile.append(card)

        log.logger.send(f"Player {self.camp} plays card {card}.", logging.DEBUG)
