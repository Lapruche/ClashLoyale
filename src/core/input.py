import logging
from typing import Callable

import pygame
import pygame._sdl2.controller as sdl2_controller
from pygame.event import Event

from constant import TRACE
from utils import log
from utils.controller_translate import translate_controller_button_to_key, translate_controller_axis_to_key, \
    release_axis_mapped_keys


def placeholder() -> None:
    """
    Placeholder function
    """
    pass


class Input:
    def __init__(self) -> None:
        """
        This module is used to handle inputs, controllers / joysticks and provide an event driven interface.
        """

        self.controllers = {}  # Registered controllers list
        self.keymaps = {
            "player_1": {
                pygame.K_q: "left",
                pygame.K_d: "right",
                pygame.K_z: "up",
                pygame.K_s: "down",
                pygame.K_SPACE: "use",
                pygame.K_e: "taunt",
            },
            "player_2": {
                pygame.K_LEFT: "left",
                pygame.K_RIGHT: "right",
                pygame.K_UP: "up",
                pygame.K_DOWN: "down",
                pygame.K_RSHIFT: "use",
                pygame.K_EXCLAIM: "taunt",
            },
        }

        # Bound input keys are added here.
        self.action_bindings = {
            "player_1": {},
            "player_2": {},
        }

        # Keys currently held down, used for continuous actions.
        self.held_keys = set()

        # Bound continuous input keys are added here.
        # We use set() to prevent duplicated, to counter running the same function more than once between frames.
        self.continuous_action_bindings = {
            "player_1": set(),
            "player_2": set(),
        }

        self.controller_id_bindings = {
            0: "player_1",
            1: "player_2"
        }

        self.controller_keymap = {
            pygame.CONTROLLER_BUTTON_DPAD_LEFT: [pygame.K_q, pygame.K_LEFT],
            pygame.CONTROLLER_BUTTON_DPAD_RIGHT: [pygame.K_d, pygame.K_RIGHT],
            pygame.CONTROLLER_BUTTON_DPAD_UP: [pygame.K_z, pygame.K_UP],
            pygame.CONTROLLER_BUTTON_DPAD_DOWN: [pygame.K_s, pygame.K_DOWN],
            pygame.CONTROLLER_BUTTON_A: [pygame.K_SPACE, pygame.K_RSHIFT],
            pygame.CONTROLLER_BUTTON_Y: [pygame.K_e, pygame.K_EXCLAIM]
        }

        # Permits getting the context keymap from a given camp.
        self.keymap_camps = {
            'rouge': self.keymaps['player_1'],
            'bleu': self.keymaps['player_2'],
        }

        sdl2_controller.init()
        controller_count = sdl2_controller.get_count()

        log.logger.send("Initialized input")
        log.logger.send(f"Got {controller_count} controllers", logging.DEBUG)

    def register_controller(self, c_id: int) -> None:
        """
        Registers a new controller.
        :param c_id: ID of the controller to register.
        """

        controller = sdl2_controller.Controller(c_id)
        self.controllers[c_id] = controller

        log.logger.send(f"Connected {controller.name}")

    def unregister_controller(self, c_id: int) -> None:
        """
        Unregisters a controller.
        :param c_id: ID of the controller to unregister.
        """

        controller = self.controllers.pop(c_id, None)
        if controller is not None:
            controller.quit()  # Controller object cleanup

        log.logger.send(f"Removed controller id {c_id}")

    def bind_action(
            self,
            context: str,
            action_name: str,
            callback: Callable[[], None] = placeholder,
            continuous: bool = False,
    ):
        """
        Binds an input key from a given keymap to a certain action.
        :param context: Context keymap to use.
        :param action_name: Semantic action name to bind to.
        :param callback: Action callback to run upon input registration.
        :param continuous: If True, run the callback every frame while the key is held.
        :return: 
        """

        if context not in self.action_bindings:
            log.logger.send(f"Tried accessing a non-existent context [{context}].", logging.ERROR)
            return

        self.action_bindings[context][action_name] = callback
        if continuous:
            self.continuous_action_bindings[context].add(action_name)
        else:
            self.continuous_action_bindings[context].discard(action_name)

        log.logger.send(f"Bound callback for action {action_name} of {context}.", TRACE)

    def run_action(self, context: str, key: int, *args: object) -> bool:
        """
        Calls the action callback from a given input bind.
        :param context: Input bind's keymap context.
        :param key: Input bind's key.
        :param args: Arguments to pass to the action callback.
        :return: False if the callback was not called, True otherwise.
        """

        action_name = self.keymaps.get(context, {}).get(key)
        if action_name is None:
            return False

        callback = self.action_bindings.get(context, {}).get(action_name)
        if callback is None:
            return False

        callback(*args)
        return True

    def run_continuous_action(self, context: str, key: int, *args: object) -> bool:
        """
        Calls the action callback only if the action is marked as continuous.
        :param context: Input bind's keymap context.
        :param key: Input bind's key.
        :param args: Arguments to pass to the action callback.
        :return: False if the callback was not called, True otherwise.
        """

        action_name = self.keymaps.get(context, {}).get(key)
        if action_name is None:
            return False

        if action_name not in self.continuous_action_bindings.get(context, set()):
            return False

        callback = self.action_bindings.get(context, {}).get(action_name)
        if callback is None:
            return False

        callback(*args)
        return True

    def run_pressed_action(self, context: str, key: int, *args: object) -> bool:
        """
        Calls the action callback only if the action is not marked as continuous.
        :param context: Input bind's keymap context.
        :param key: Input bind's key.
        :param args: Arguments to pass to the action callback.
        :return: False if the callback was not called, True otherwise.
        """

        action_name = self.keymaps.get(context, {}).get(key)
        if action_name is None:
            return False

        if action_name in self.continuous_action_bindings.get(context, set()):
            return False

        callback = self.action_bindings.get(context, {}).get(action_name)
        if callback is None:
            return False

        callback(*args)
        return True

    def process(self, events: list[Event]) -> None:
        """
        Processes pygame input events, to be run in the main loop.
        :param events: Events to process
        """

        for event in events:
            match event.type:
                case pygame.KEYDOWN:
                    self.held_keys.add(event.key)
                    self.run_pressed_action('player_1', event.key) or self.run_pressed_action('player_2', event.key)
                case pygame.KEYUP:
                    self.held_keys.discard(event.key)
                case pygame.CONTROLLERDEVICEADDED:
                    if sdl2_controller.is_controller(event.device_index):
                        self.register_controller(event.device_index)
                case pygame.CONTROLLERDEVICEREMOVED:
                    self.unregister_controller(event.instance_id)
                case pygame.CONTROLLERBUTTONDOWN:
                    translated = translate_controller_button_to_key(self.controller_keymap, event)
                    if translated is None:
                        continue

                    plr_keymap, key = translated
                    self.held_keys.add(key)
                    self.run_pressed_action(plr_keymap, key)
                case pygame.CONTROLLERBUTTONUP:
                    translated = translate_controller_button_to_key(self.controller_keymap, event)
                    if translated is None:
                        continue

                    _, key = translated
                    self.held_keys.discard(key)
                case pygame.CONTROLLERAXISMOTION:
                    player_index = 0 if event.instance_id == 0 else 1
                    release_axis_mapped_keys(self.controller_keymap, event.axis, player_index, self.held_keys)
                    key = translate_controller_axis_to_key(self.controller_keymap, event)

                    if key is not None:
                        self.held_keys.add(key)

        for key in self.held_keys:
            self.run_continuous_action('player_1', key) or self.run_continuous_action('player_2', key)
