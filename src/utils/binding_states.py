from typing import Callable

from core.input import pass_f
from levels.Arena.arena_renderer import taunt
from managers.cursor_manager import Cursor
from managers.player import Player


def bind_default_actions(modules: dict, start_placing_callback: Callable[[], None], player: Player) -> None:
    player_context = player.keymap_context
    input_module = modules["input"]
    ui_module = modules["ui"]
    sound_module = modules["sound"]

    input_module.bind_action(player_context, "up", pass_f)
    input_module.bind_action(player_context, "left", pass_f)
    input_module.bind_action(player_context, "right", pass_f)
    input_module.bind_action(player_context, "down", pass_f)
    input_module.bind_action(player_context, "use", start_placing_callback)
    input_module.bind_action(player_context, "taunt", lambda: taunt(ui_module.screen, sound_module, player.camp))


def bind_placement_actions(confirm_placement_callback: Callable[[Player, Cursor], None], player: Player,
                           modules: dict) -> None:
    input_module = modules["input"]
    ui_module = modules["ui"]
    sound_module = modules["sound"]

    input_module.bind_action(player.keymap_context, "up", lambda: player.cursor.move("up"))
    input_module.bind_action(player.keymap_context, "left", lambda: player.cursor.move("left"))
    input_module.bind_action(player.keymap_context, "right", lambda: player.cursor.move("right"))
    input_module.bind_action(player.keymap_context, "down", lambda: player.cursor.move("down"))
    input_module.bind_action(player.keymap_context, "use", confirm_placement_callback)
