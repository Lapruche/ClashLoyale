import logging

from constant import TRACE
from core import asset
from utils import log
from utils.scale_card import scale_card


class Player:
    def __init__(self, camp, deck, elixir_start) -> None:
        self.camp = camp
        self.deck = deck
        self.elixir = elixir_start
        self.deck_img = self._get_cards_img()

    def _get_cards_img(self):
        cards = []
        for carte in self.deck:
            card = asset.get_image_stem(carte)
            if card:
                card = scale_card(card, 8, 6.5)
                cards.append(card)

        log.logger.send(f"Populated card images for player {self.camp}.", logging.DEBUG)
        return cards

    def modify_elixir(self, amount):
        self.elixir = max(0, min(10, self.elixir + amount))
        log.logger.send(f"Modified elixir for player {self.camp} to {self.elixir}.", TRACE)
