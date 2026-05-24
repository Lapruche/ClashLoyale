from core.sound import Sound
from managers.Unit.unit_ability import UnitAbility
from utils.tile_helper import tile_to_pixel


class Attack(UnitAbility):
    def __init__(self, sound_module: Sound, damage: int = 10, attacks_per_second: float = 1.5,
                 attack_range: float = 5.0, sfx=None) -> None:
        cooldown = 1 / attacks_per_second if attacks_per_second > 0 else float("inf")
        super().__init__(sound_module, "attack", cooldown)
        self.damage: int = damage
        self.attack_range: float = attack_range
        self.sfx = sfx

    def execute(self, caster, target) -> None:
        if caster.distance_to(target.pos) <= tile_to_pixel(self.attack_range):
            caster.play_animation("hit", True)
            target.take_damage(self.damage)

            if self.sfx is not None:
                self.sound_module.play_sound(self.sfx)
                
            self._timer = self.cooldown  # Resets the cooldown
