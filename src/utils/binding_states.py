from core.input import placeholder
from levels.Arena import card_placement
from levels.Arena.arena_renderer import taunt
from managers.Player.player import Player
from managers.Unit.unit_manager import UnitManager


class BindingsHelper:
    def __init__(self, modules, unit_manager: UnitManager) -> None:
        self.modules = modules
        self.unit_manager = unit_manager
        self.input = modules["input"]
        self.ui = modules["ui"]
        self.sound = modules["sound"]

    def bind_default_actions(self, player: Player) -> None:
        """
        Sets all binds to placeholder actions (practically, it just unbinds them).
        :param player: Player to bind actions to
        """

        self.input.bind_action(player.keymap_context, "up", placeholder)
        self.input.bind_action(player.keymap_context, "left", placeholder)
        self.input.bind_action(player.keymap_context, "right", placeholder)
        self.input.bind_action(player.keymap_context, "down", placeholder)
        self.input.bind_action(player.keymap_context, "use", placeholder)
        self.input.bind_action(player.keymap_context, "taunt", placeholder)

    def bind_ingame_actions(self, player: Player) -> None:
        """
        Sets all binds to in-game actions.
        :param player: Player to bind actions to
        """

        self.input.bind_action(player.keymap_context, "up", lambda: player.cursor.move("up"))
        self.input.bind_action(player.keymap_context, "left", lambda: player.cursor.move("left"))
        self.input.bind_action(player.keymap_context, "right", lambda: player.cursor.move("right"))
        self.input.bind_action(player.keymap_context, "down", lambda: player.cursor.move("down"))
        self.input.bind_action(player.keymap_context, "use",
                               lambda: card_placement.place(self.modules, self, self.unit_manager, player))
        self.input.bind_action(player.keymap_context, "taunt", lambda: taunt(self.ui.screen, self.sound, player.camp))

    def bind_placing_actions(self, player: Player) -> None:
        """
        Sets all binds to in-game placing actions.
        :param player: Player to bind actions to
        """

        self.input.bind_action(player.keymap_context, "up", lambda: player.cursor.move("up"), continuous=True)
        self.input.bind_action(player.keymap_context, "left", lambda: player.cursor.move("left"), continuous=True)
        self.input.bind_action(player.keymap_context, "right", lambda: player.cursor.move("right"), continuous=True)
        self.input.bind_action(player.keymap_context, "down", lambda: player.cursor.move("down"), continuous=True)
