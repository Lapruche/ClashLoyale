from typing import Any

import pygame

from constant import CONTROLLER_DEADZONE


def get_keymap_from_instance_id(instance_id: int):
    return "player_1" if instance_id == 0 else "player_2"


def translate_axis_value_to_key(controller_keymap: dict[int, list[int]], event: pygame.event.Event, plr_index: int,
                                negative_button: int, positive_button: int) -> int | None:
    """
    Translates the axis value to its corresponding key. 
    :param controller_keymap: Controller keymap.
    :param event: Event to translate. 
    :param plr_index: Player index.
    :param negative_button: Button to call for a negative axis value.
    :param positive_button: Button to call for a positive axis value.
    :return: The corresponding key. None if the axis value is within CONTROLLER_DEADZONE.
    """

    if event.value > CONTROLLER_DEADZONE:
        return controller_keymap[positive_button][plr_index]
    elif event.value < -CONTROLLER_DEADZONE:
        return controller_keymap[negative_button][plr_index]
    else:
        return None


def get_axis_mapped_keys(controller_keymap: dict[int, list[int]], axis: int, plr_index: int) -> tuple[
                                                                                                    int, int] | None:
    """
    Gets the negative and positive mapped keys from a given axis.
    :param controller_keymap: Controller keymap.
    :param axis: Controller axis.
    :param plr_index: Player index.
    :return: The corresponding keys for negative and positive axis values. None if it is an unknown axis.
    """

    if axis == 0:
        return (
            controller_keymap[pygame.CONTROLLER_BUTTON_DPAD_LEFT][plr_index],
            controller_keymap[pygame.CONTROLLER_BUTTON_DPAD_RIGHT][plr_index],
        )
    if axis == 1:
        return (
            controller_keymap[pygame.CONTROLLER_BUTTON_DPAD_DOWN][plr_index],
            controller_keymap[pygame.CONTROLLER_BUTTON_DPAD_UP][plr_index],
        )

    return None


def release_axis_mapped_keys(controller_keymap: dict[int, list[int]], axis: int, plr_index: int,
                             held_keys: set[Any]) -> None:
    """
    Releases the axis mapped keys from all known axis.
    :param controller_keymap: Controller keymap.
    :param axis: Controller axis.
    :param plr_index: Player index.
    :param held_keys: Set of currently held keys.
    :return: 
    """
    axis_keys = get_axis_mapped_keys(controller_keymap, axis, plr_index)
    if axis_keys is None:
        return

    for key in axis_keys:
        held_keys.discard(key)


def translate_controller_button_to_key(controller_keymap: dict[int, list[int]], event: pygame.event.Event) -> tuple[
                                                                                                                  str, int] | None:
    """
    Translates the controller button event to a keyboard key 
    with its corresponding keymap depending on the controller's ID.
    :param controller_keymap: 
    :param event: Event to translate 
    :return: The corresponding keymap, and key. None if the event button is unknown.
    """

    if event.button not in controller_keymap.keys():
        return None
    translated_keys = controller_keymap[event.button]

    if event.instance_id == 0:
        return "player_1", translated_keys[0]
    else:
        return "player_2", translated_keys[1]


def translate_controller_axis_to_key(controller_keymap: dict[int, list[int]], event: pygame.event.Event) -> int | None:
    """
    Translates the controller axis event to a keyboard key.
    :param controller_keymap: Controller keymap.
    :param event: Event to translate 
    :return: The corresponding key. None if the event axis is unknown or couldn't be translated.
    """

    player_index = 0 if event.instance_id == 0 else 1  # Prevent out of bounds index

    if event.axis == 0:
        key = translate_axis_value_to_key(controller_keymap, event, player_index,
                                          pygame.CONTROLLER_BUTTON_DPAD_LEFT,
                                          pygame.CONTROLLER_BUTTON_DPAD_RIGHT)
    elif event.axis == 1:
        key = translate_axis_value_to_key(controller_keymap, event, player_index,
                                          pygame.CONTROLLER_BUTTON_DPAD_UP,
                                          pygame.CONTROLLER_BUTTON_DPAD_DOWN)
    else:
        return None

    if key is None:
        return None

    return key
