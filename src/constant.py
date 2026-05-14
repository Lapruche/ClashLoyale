import logging
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent

SOUNDS_PATH = BASE_DIR / "sounds"
MUSIC_THEMES_PATH = SOUNDS_PATH / "themes"
SPRITES_PATH = BASE_DIR / "sprites"
CARDS_PATH = SPRITES_PATH / "cartes"
WIDGETS_PATH = SPRITES_PATH / "widgets"
FONTS_PATH = BASE_DIR / "fonts"
DEFINITIONS_PATH = BASE_DIR / "units" /"definitions"
GUI_PATH = SPRITES_PATH / "GUI"
TEXT_COLOR = "#EEEEEE"
BACKGROUND_COLOR = "#202020"
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000

BLUE_COLOR = "#0099FF"
RED_COLOR = "#FF5500"
ELIXIR_COLOR = "#CC00BB"

CARD_OFFSET_Y = 10

MAX_PLAYER_COUNT = 2
DECK_LENGTH = 8

TRACE = 5

LOG_COLORS = {
    TRACE: '\033[37m',
    logging.DEBUG: '\033[36m',  # Cyan
    logging.INFO: '\033[32m',  # Green
    logging.WARNING: '\033[33m',  # Yellow
    logging.ERROR: '\033[31m',  # Red
    logging.CRITICAL: '\033[35m',  # Magenta
}

LOG_COLORS_RESET = '\033[0m'
