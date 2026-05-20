import logging

import pygame

from managers.Unit import unit_dict
from managers.Unit.unit_utils import get_definition
from managers.Unit.units.knight import Knight
from utils import log
from utils.drawing import scale_unit


class UnitManager:
    def __init__(self, bounds_rect):
        self.bounds_rect = bounds_rect
        self.units = []
        self.next_id = 0

    def spawn_unit(self, unit_name: str, camp: str, pos: tuple):
        definitions = get_definition(unit_name)
        if definitions is None:
            log.logger.send(f"No definition for unit {unit_name} found.", logging.ERROR)
            return

        unit_class = unit_dict.UNITS_DICT.get(unit_name, Knight)
        unit = unit_class(self.next_id, camp, definitions, pos)
        self.units.append(unit)
        unit.on_spawn()

        self.next_id += 1  # Increments id for next unit to prevent duplicates

        log.logger.send(f"Added {unit_name} to board.", logging.DEBUG)

    def draw(self, screen: pygame.Surface):
        for unit in self.units:
            sprite = scale_unit(unit.current_sprite, (3, 3))
            if sprite is None:
                log.logger.send(f"Unit {unit.name}:{unit.id} has no sprite and cannot be drawn.", logging.ERROR)
                continue

            screen.blit(sprite, sprite.get_rect(center=(unit.pos[0], unit.pos[1])))

    def tick(self, dt):
        # Health check

        for unit in self.units:
            unit.update(dt, [e for e in self.units if e.camp != unit.camp])
            if unit.health <= 0:
                unit.on_death()
                self.units.remove(unit)
                log.logger.send(f"Removing unit {unit.id} from board as he died.", logging.DEBUG)
