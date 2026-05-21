from constant import UNIT_SOUNDS_PATH
from managers.Unit.abilities.attack import Attack
from managers.Unit.game_unit import GameUnit
from utils.path_animate import unit_animation


class KingTower(GameUnit):
    def __init__(self, modules: dict, unit_id: int, camp: str, properties: dict, pos: tuple):
        super().__init__(modules, camp, unit_id, properties, pos)
        self.add_ability(
            Attack(modules["sound"], damage=self._properties["damage"], attacks_per_second=self._properties["freq_atk"],
                   attack_range=self._properties["range"], sfx=UNIT_SOUNDS_PATH / "canon_fire.wav"))
        self._animator.register_animation("stand",
                                          unit_animation(self.name, "stand", camp, self._properties["freq_atk"]))
        self._animator.register_animation("hit",
                                          unit_animation(self.name, "hit", camp, self._properties["freq_atk"]))
        self._animator.play("stand")
        self.alarmed = False

    def on_update(self, dt: float, enemies) -> None:
        if len(enemies) != 0:
            if not self.alarmed and self.health != self._properties["pv"]:
                self.alarmed = True
                self.modules["sound"].play_sound(UNIT_SOUNDS_PATH / "declenchement.wav", 0.5)

                nearest = min(enemies, key=lambda x: x.distance_to(self.pos))
                self.use_ability("attack", nearest)
