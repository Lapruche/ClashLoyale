from constant import GUI_SOUNDS_PATH
from managers import cursor_manager
from managers.player import Player
from utils.binding_states import bind_default_actions


class CardPlacementHandler:
    def __init__(self, modules):
        self.modules = modules
        self.input = modules["input"]
        self.sound = modules["sound"]

    def start_placing(self, player, card_index):
        cursor = cursor_manager.get_cursor(player.camp)
        if cursor is None:
            return

        cursor.placing = True
        cursor.card_index = card_index  # Saves the card index for later use

        self.sound.play_sound(GUI_SOUNDS_PATH / "elixir.wav", 0.3)

        
    def confirm_placement(self, player: Player, cursor):
        card = player.play_card(self.sound, cursor)
        
        bind_default_actions(player.cursor, self.modules)
