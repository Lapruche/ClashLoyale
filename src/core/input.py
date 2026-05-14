import logging

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
        self.keymaps = {  # TODO: Use semantic action names instead (ex: "use", "taunt", "forward")
            'player_1': {
                pygame.K_q: pass_f,
                pygame.K_d: pass_f,
                pygame.K_z: pass_f,
                pygame.K_s: pass_f,
                pygame.K_SPACE: pass_f,  # Use
                pygame.K_e: pass_f,  # Taunt
            },
            'player_2': {
                pygame.K_LEFT: pass_f,
                pygame.K_RIGHT: pass_f,
                pygame.K_UP: pass_f,
                pygame.K_DOWN: pass_f,
                pygame.K_RSHIFT: pass_f,  # Use
                pygame.K_EXCLAIM: pass_f,  # Taunt
            },
            'controller': {  # 
                13: pass_f_c,  # Left
                14: pass_f_c,  # Right
                11: pass_f_c,  # Up
                12: pass_f_c,  # Down
                0: pass_f_c,  # Use
                3: pass_f_c  # Taunt
            }
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

    def bind_action(self, keymap, key, action=pass_f):
        if keymap not in self.keymaps.keys():
            log.logger.send(f"Tried accessing a non-existent keymap [{keymap}].", logging.ERROR)
            return

        registered_keymap = self.keymaps[keymap]

        if key not in registered_keymap.keys():
            log.logger.send(f"Tried binding a non-existent key ({key}).", logging.ERROR)
            return

        registered_keymap[key] = action
        log.logger.send(f"Bound action to key {key}.", TRACE)

    def run_action(self, keymap, key, *args):
        action = self.keymaps.get(keymap, {}).get(key)
        if action is None:
            return False

        action(*args)
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
                        self.run_action('controller', event.button, controller)
