import logging

from constant import DECK_LENGTH, MAX_PLAYER_COUNT
from managers.cursor_manager import Cursor
from managers.player import Player
from utils import log

players: list[Player] = []


def add_player(keymap_context: str, cursor: Cursor, camp, deck, elixir_start):
    if len(players) >= MAX_PLAYER_COUNT:
        log.logger.send("Cannot add player, reached max player count.", logging.ERROR)
        return None

    for plr in players:
        if plr.camp == camp:
            log.logger.send(f"Cannot add player, side {camp} is already taken.", logging.ERROR)
            return None

    if len(deck) < DECK_LENGTH:
        log.logger.send(f"Cannot add player, deck doesn't meet required length.", logging.ERROR)

    player = Player(keymap_context, cursor, camp, deck, elixir_start)
    player.populate_deck()

    players.append(player)
    log.logger.send(f"Registered player {camp}.", logging.DEBUG)

    return player


def get_player(camp) -> Player | None:
    for plr in players:
        if plr.camp == camp:
            return plr
    return None


def reset():
    players.clear()  # Remove all registered players
    log.logger.send("Reset card decks.", logging.DEBUG)
