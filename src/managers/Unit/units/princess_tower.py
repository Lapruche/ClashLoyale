from constant import UNIT_SOUNDS_PATH
from managers.Unit.abilities.attack import Attack
from managers.Unit.game_unit import GameUnit
from utils.path_animate import unit_animation


class PrincessTower(GameUnit):
    def __init__(self, modules: dict, unit_id: int, camp: str, properties: dict, pos: tuple):
        super().__init__(modules, camp, unit_id, properties, pos)
        self.add_ability(
            Attack(modules["sound"], damage=self._properties["damage"], attacks_per_second=self._properties["freq_atk"],
                   attack_range=self._properties["range"], sfx=UNIT_SOUNDS_PATH / "bow_shoot.wav"))
        stand_animation = unit_animation(self.name, "stand", camp, self._properties["freq_atk"])
        self._animator.register_animation("stand",
                                          stand_animation)
        self._animator.register_animation("hit",
                                          stand_animation)  # Dummy stand animation because there's no hit sprites
        self._animator.play("stand")

    def on_update(self, dt: float, enemies) -> None:
        if len(enemies) != 0:
            nearest = min(enemies, key=lambda x: x.distance_to(self.pos))
            self.use_ability("attack", nearest)
