from constant import SCREEN_HEIGHT, SCREEN_WIDTH, TRACE
from managers.Player.player import Player
from managers.Unit.unit_manager import UnitManager
from utils import log


def place(modules: dict, bindings_helper, unit_manager: UnitManager, player: Player):
    sound = modules["sound"]
    cursor = player.cursor

    if not cursor.placing:
        cursor.placing = True
        bindings_helper.bind_placing_actions(player)

        log.logger.send(f"Player {player.camp} started placing.", TRACE)
    else:
        cursor.placing = False
        bindings_helper.bind_ingame_actions(player)

        unit_name = player.hand[cursor.card_index]
        unit_pos = (SCREEN_WIDTH / 2 + cursor.pos[0], SCREEN_HEIGHT / 2 + cursor.pos[1])

        unit_manager.spawn_unit(unit_name, player.camp, unit_pos)
        player.play_card(sound, cursor.card_index, unit_pos)
        
        log.logger.send(f"Player {player.camp} placed a card.", TRACE)
