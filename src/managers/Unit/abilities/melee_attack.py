import logging

from managers.Unit.unit_ability import UnitAbility
from utils import log
from utils.tile_helper import tile_to_pixel


class MeleeAttack(UnitAbility):
    def __init__(self, damage: int = 10, cooldown: float = 1.5, attack_range: float = 5.0) -> None:
        super().__init__("melee_attack", cooldown)
        self.damage: int = damage
        self.attack_range: float = attack_range

    def execute(self, caster, target) -> None:
        if caster.distance_to(target.pos) <= tile_to_pixel(self.attack_range):
            caster.play_animation("hit", True)
            target.take_damage(self.damage)
            self._timer = self.cooldown

            log.logger.send("Executed MeleeAttack !!!", logging.DEBUG)
