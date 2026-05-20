import logging
from typing import Callable

import pygame
from pygame.event import Event

from constant import TRACE
from utils import log


def pass_f():  # Placeholder function
    pass


def pass_f_c(device):  # Placeholder controller function
    print(f"Controller {device.get_name()} pressed smth")


class Input:
    def __init__(self):
        self.controllers = {}
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

        self.action_bindings = {
            "player_1": {},
            "player_2": {},
        }

        self.keymap_camps = {
            'rouge': self.keymaps['player_1'],
            'bleu': self.keymaps['player_2'],
        }

        pygame.joystick.init()
        joystick_count = pygame.joystick.get_count()

        log.logger.send("Initialized input")
        log.logger.send(f"Got {joystick_count} controllers", logging.DEBUG)

        for i in range(joystick_count):
            self.register_controller(i)

    def register_controller(self, c_id):
        controller = pygame.joystick.Joystick(c_id)
        controller.init()
        self.controllers[c_id] = controller

        log.logger.send(f"Connected {controller.get_name()}")

    def unregister_controller(self, joy_id):
        self.controllers.pop(joy_id, pass_f)
        log.logger.send(f"Removed controller id {joy_id}")

    def bind_action(self, context: str, action_name: str, callback: Callable[[], None] = pass_f):
        """

        :param context: Context keymap to use
        :param action_name: Semantic action name to bind to
        :param callback: 
        :return: 
        """
        if context not in self.action_bindings:
            log.logger.send(f"Tried accessing a non-existent context [{context}].", logging.ERROR)
            return

        self.action_bindings[context][action_name] = callback

        log.logger.send(f"Bound callback for action {action_name} of {context}.", TRACE)


    def run_action(self, context, key, *args):
        action_name = self.keymaps.get(context, {}).get(key)
        if action_name is None:
            return False

        callback = self.action_bindings.get(context, {}).get(action_name)
        if callback is None:
            return False

        callback(*args)
        return True

    def process(self, events: list[Event]):
        for event in events:
            match event.type:
                case pygame.JOYDEVICEADDED:
                    self.register_controller(event.device_index)
                case pygame.JOYDEVICEREMOVED:
                    self.unregister_controller(event.instance_id)
                case pygame.KEYDOWN:
                    self.run_action('player_1', event.key) or self.run_action('player_2', event.key)
                case pygame.JOYBUTTONDOWN:
                    controller = self.controllers.get(event.instance_id)
                    if controller:
                        #TODO self.run_action('controller', event.button, controller)
                        pass