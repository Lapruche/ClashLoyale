import logging
from enum import Enum
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

ASSETS_PATH = BASE_DIR / "assets"
SOUNDS_PATH = ASSETS_PATH / "sounds"
UNIT_SOUNDS_PATH = SOUNDS_PATH / "unit"
GUI_SOUNDS_PATH = SOUNDS_PATH / "gui"
MUSIC_THEMES_PATH = SOUNDS_PATH / "themes"
SPRITES_PATH = ASSETS_PATH / "sprites"
BLUE_SPRITES = SPRITES_PATH / "blue_units"
RED_SPRITES = SPRITES_PATH / "red_units"
CARDS_PATH = SPRITES_PATH / "cartes"
WIDGETS_PATH = SPRITES_PATH / "widgets"
FONTS_PATH = ASSETS_PATH / "fonts"
DEFINITIONS_PATH = ASSETS_PATH / "unit_definitions"
GUI_PATH = SPRITES_PATH / "GUI"
TEXT_COLOR = "#EEEEEE"
BACKGROUND_COLOR = "#202020"
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000

BLUE_COLOR = "#0099FF"
RED_COLOR = "#FF2200"
ELIXIR_COLOR = "#CC00BB"

CARD_OFFSET_Y = 10

TILE_SIZE = 25
CURSOR_SPEED = 5
START_ELIXIR = 6
MAX_PLAYER_COUNT = 2
DECK_LENGTH = 8

HP_BAR_SCALE = (2, 2)
HP_BAR_OFFSET = 4
HP_BAR_SPRITES_COUNT = 17

TRACE = 5


class UnitState(Enum):
    STANDING = 0
    WALKING = 1
    RUNNING = 2
    ATTACKING = 3
    DEAD = 4

LOG_COLORS = {
    TRACE: '\033[37m',
    logging.DEBUG: '\033[36m',  # Cyan
    logging.INFO: '\033[32m',  # Green
    logging.WARNING: '\033[33m',  # Yellow
    logging.ERROR: '\033[31m',  # Red
    logging.CRITICAL: '\033[35m',  # Magenta
}

LOG_COLORS_RESET = '\033[0m'
