from managers.Unit.abilities.melee_attack import MeleeAttack
from managers.Unit.game_unit import GameUnit
from utils.path_animate import unit_animation


class Knight(GameUnit):
    def __init__(self, unit_id: int, camp: str, properties: dict, pos: tuple):
        super().__init__(camp, unit_id, properties, pos)

        self.add_ability(MeleeAttack(damage=self._properties["damage"], cooldown=self._properties["freq_atk"],
                                     attack_range=self._properties["range"]))

        self._animator.register_animation("stand", unit_animation(self.name, "stand", camp, 1, True))
        self._animator.register_animation("hit", unit_animation(self.name, "hit", camp, 0.15))
        self._animator.register_animation("run", unit_animation(self.name, "run", camp, 1, True))
        self._animator.play("stand")

    def on_update(self, dt: float, enemies: list[GameUnit]):
        if len(enemies) != 0:
            nearest = min(enemies, key=lambda x: x.distance_to(self.pos))  # Gets the closest enemy to the unit.
            self.use_ability("melee_attack", nearest)

    def on_death(self) -> None:
        print("bro died")
