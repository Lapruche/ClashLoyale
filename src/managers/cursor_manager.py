# Prototype by draco1661 <draco1661@proton.me>

from core.sound import Sound
from managers import player_manager

cursors = []


class Cursor:
    def __init__(self, camp) -> None:
        self.camp = camp
        self.pos = (0, 0)
        self.placing = False
        self.card_index = 0

    def move(self, direction: str):
        if direction == "left":
            self.pos[0] -= 1
        if direction == "right":
            self.pos[0] += 1
        if direction == "up":
            self.pos[1] -= 1
        if direction == "down":
            self.pos[1] += 1

    def confirm(self, sound_module: Sound, card_index: int) -> None:
        plr = player_manager.get_player(self.camp)
        if plr is None:
            return None

        plr.play_card(sound_module, card_index)
        self.placing = False
        return None


def get_cursor(camp) -> Cursor | None:
    for cursor in cursors:
        if cursor.camp == camp:
            return cursor
    return None


def init_arena_cursors():
    cursors.clear()
    red_cursor = Cursor("rouge")
    bleu_cursor = Cursor("bleu")
    cursors.append(red_cursor)
    cursors.append(bleu_cursor)
