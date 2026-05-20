# Prototype by draco1661 <draco1661@proton.me>

from core.sound import Sound
from managers import player_manager

cursors = []


class Cursor:
    def __init__(self, camp) -> None:
        self.camp = camp
        self.pos = [0, 0]
        self.placing = False
        self.card_index = 0

    def move(self, direction: str):
        if self.placing:
            if direction == "left":
                self.pos[0] -= 3
            if direction == "right":
                self.pos[0] += 3
            if direction == "up":
                self.pos[1] -= 3
            if direction == "down":
                self.pos[1] += 3
        else:
            if direction == "up":
                self.card_index = (self.card_index - 1) % 4
            elif direction == "down":
                self.card_index = (self.card_index + 1) % 4

            if self.card_index >= 5:
                self.card_index = 0


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
