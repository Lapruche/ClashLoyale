from constant import GUI_SOUNDS_PATH, TRACE
from managers.player import Player
from utils import log


def place(modules: dict, bindings_helper, player: Player):
    sound = modules["sound"]
    cursor = player.cursor

    if not cursor.placing:
        cursor.placing = True
        bindings_helper.bind_placing_actions(player)
        log.logger.send(f"Player {player.camp} started placing.", TRACE)
    else:
        player.play_card(sound, cursor.card_index, cursor.pos)
        sound.play_sound(GUI_SOUNDS_PATH / "elixir.wav", 0.3)
        cursor.placing = False
        
        bindings_helper.bind_ingame_actions(player)
        
        log.logger.send(f"Player {player.camp} placed a card.", TRACE)