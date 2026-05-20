import logging

from managers.Unit.game_unit import GameUnit
from managers.Unit.unit import get_definition
from utils import log


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

        unit = GameUnit(camp, self.next_id, definitions, pos)
        self.units.append(unit)
        unit.on_spawn()

        log.logger.send("Added unit to board.", logging.DEBUG)

    def draw(self):
        for unit in self.units:
            pass  # TODO

    def tick(self):
        # Health check

        for unit in self.units:
            if unit.health <= 0:
                unit.on_death()
                self.units.remove(unit)
                log.logger.send(f"Removing unit {unit.id} from board as he died.", logging.DEBUG)
