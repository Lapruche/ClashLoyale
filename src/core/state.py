from enum import IntEnum

from constant import TRACE
from utils import log


class GameState(IntEnum):
    STARTING = 0
    MENU = 1
    DECK_SELECTION = 2
    GAME = 3
    PAUSED = 4
    END_GAME = 5
    EXIT = 6
    TEST = 7


class StateManager:
    def __init__(self, initial_state: GameState, screens: dict | None = None):
        self.state = initial_state
        self.screens = screens or {}

    def run_screen(self, dt=0):
        return self.screens[self.state].run(dt)

    def get_state(self):
        return self.state

    def set_state(self, new_state):
        self.state = new_state
        log.logger.send(f"Set new state {new_state}", TRACE)
        return self.screens[self.state].start()
