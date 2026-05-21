import logging

import pygame

from constant import SPRITES_PATH, HP_BAR_SCALE, HP_BAR_OFFSET
from core import asset
from managers.Unit import unit_dict
from managers.Unit.unit_utils import get_properties
from managers.Unit.units.knight import Knight
from utils import log
from utils.drawing import scale_by_size
from utils.path_helper import path_number


class UnitManager:

    def __init__(self, modules: dict, bounds_rect):
        self.modules = modules
        self.bounds_rect = bounds_rect
        self.units = []
        self.hpbar_sprites_red = []
        self.hpbar_sprites_blue = []
        self.next_id = 0

    def init_hpbar_sprites(self):
        self.hpbar_sprites_red = self._load_hpbar_sprites("rouge")
        self.hpbar_sprites_blue = self._load_hpbar_sprites("bleu")
        log.logger.send("Loaded hpbar sprites.", logging.DEBUG)

    def _load_hpbar_sprites(self, camp: str) -> list[pygame.Surface]:
        hpbar_path = SPRITES_PATH / "hp_bar" / camp
        sprites = sorted(hpbar_path.glob("*.png"), key=path_number)
        return [scale_by_size(asset.get_image(sprite), HP_BAR_SCALE) for sprite in sprites]

    def spawn_unit(self, unit_name: str, camp: str, pos: tuple):
        definitions = get_properties(unit_name)
        if definitions is None:
            log.logger.send(f"No definition for unit {unit_name} found.", logging.ERROR)
            return

        unit_class = unit_dict.UNITS_DICT.get(unit_name, Knight)
        unit = unit_class(self.modules, self.next_id, camp, definitions, pos)
        self.units.append(unit)
        unit.on_spawn()

        self.next_id += 1  # Increments id for next unit to prevent duplicates

        log.logger.send(f"Added {unit_name} to board.", logging.DEBUG)

    def draw(self, screen: pygame.Surface):
        for unit in self.units:
            sprite = scale_by_size(unit.current_sprite, (3, 3))
            if sprite is None:
                log.logger.send(f"Unit {unit.name}:{unit.id} has no sprite and cannot be drawn.", logging.ERROR)
                continue

            unit_rect = sprite.get_rect(center=unit.pos)
            screen.blit(sprite, unit_rect)

            # HP bar
            hp_sprite_index = unit.hpbar_sprite_index
            if hp_sprite_index is not None:
                hp_sprites = None
                if unit.camp == "bleu":
                    hp_sprites = self.hpbar_sprites_blue
                elif unit.camp == "rouge":
                    hp_sprites = self.hpbar_sprites_red

                if hp_sprites and hp_sprite_index < len(hp_sprites):
                    hp_sprite = hp_sprites[hp_sprite_index]
                    hp_rect = hp_sprite.get_rect(midbottom=(unit_rect.centerx, unit_rect.top - HP_BAR_OFFSET))
                    screen.blit(hp_sprite, hp_rect)

    def tick(self, dt):
        # Health check

        for unit in self.units:
            unit.update(dt, [e for e in self.units if e.camp != unit.camp])
            if unit.health <= 0:
                unit.on_death()
                self.units.remove(unit)
                log.logger.send(f"Removing unit {unit.name}:{unit.id} from board as it died.", logging.DEBUG)
