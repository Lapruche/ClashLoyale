import math
from abc import ABC

from constant import TRACE, UnitState, HP_BAR_SPRITES_COUNT
from managers.Unit.unit_ability import UnitAbility
from managers.Unit.unit_animator import UnitAnimator
from utils import log


class GameUnit(ABC):
    def __init__(self, modules: dict, camp: str, unit_id: int, properties: dict, pos: tuple):
        """
        Game unit's main abstract class.
        :param modules: Game modules.
        :param camp: Unit's side.
        :param unit_id: Unit's ID.
        :param properties: Unit's properties.
        :param pos: Unit's starting position.
        """

        self.modules = modules
        self.camp = camp
        self.id = unit_id
        self._properties = properties

        self.name = self._properties["name"]
        self.health = self._properties["pv"]  # Current health

        self.pos = [pos[0], pos[1]]
        self.state: UnitState = UnitState.STANDING  # Current state

        self._abilities: dict[str, UnitAbility] = {}
        self._animator: UnitAnimator = UnitAnimator()

        self.target = None

    @property
    def current_sprite(self):
        return self._animator.current_sprite

    @property
    def hpbar_sprite_index(self):
        max_health = self._properties["pv"]
        if max_health <= 0 or self.health >= max_health:
            return None

        health_ratio = max(0, min(1, self.health / max_health))
        missing_health_ratio = 1 - health_ratio
        return min(HP_BAR_SPRITES_COUNT - 1, math.ceil(missing_health_ratio * (HP_BAR_SPRITES_COUNT - 1)))

    def take_damage(self, amount) -> None:
        """
        Takes a given amount of damage.
        :param amount: Amount of damage.
        """

        self.health = max(0, self.health - amount)
        log.logger.send(f"Unit {self.id} took {amount} damage.", TRACE)

    def move(self, delta_pos: tuple):
        """
        Moves the unit to the new position. 
        :param delta_pos: Delta position.
        """

        self.pos[0] += delta_pos[0]
        self.pos[1] += delta_pos[1]
        self._animator.play("run")

    def distance_to(self, pos: tuple | list) -> float:
        return math.dist(self.pos, pos)

    def play_animation(self, name: str, force_check: bool = False) -> None:
        self._animator.play(name, force_check)

    def add_ability(self, ability: UnitAbility):
        self._abilities[ability.name] = ability

    def use_ability(self, ability_name, target):
        ability = self._abilities.get(ability_name)
        if ability and ability.is_ready():
            ability.execute(self, target)

    def update(self, dt, enemies):
        self._animator.update(dt)

        # Updates timer for each ability
        for ability in self._abilities.values():
            ability.update(dt)

        # Calls the abstract method
        self.on_update(dt, enemies)

    def on_spawn(self) -> None:
        """
        Called upon unit's spawn. 
        """
        ...

    def on_death(self) -> None:
        """
        Called upon unit's death. 
        """
        ...

    def on_update(self, dt: float, enemies) -> None:
        """
        Called upon unit's update. 
        :param dt: DeltaTime.
        :param enemies: List of enemies.
        """
        ...

    """
    def pathfinding(self):
        dx = ennemi[0] - moi[0]
        dy = ennemi[1] - moi[1]
        radians = math.atan2(dy, dx)
        degres = math.degrees(radians)
        return degres

    def tageting(self):
        if self.camp == "rouge":
            bestID = None
            best_distance = 100000
            cpt = 0
            for unit in blue:
                cpt += 1
                if distance(blue[cpt].x, blue[cpt].y) < 1000:
                    if distance(blue[cpt].x, blue[cpt].y) < best_distance:
                        bestID = blue[cpt].id
            return bestID
        else:
            bestID = None
            best_distance = 100000
            cpt = 0
            for unit in red:
                cpt += 1
                if distance(red[cpt].x, red[cpt].y) < 1000:
                    if distance(red[cpt].x, red[cpt].y) < best_distance:
                        bestID = red[cpt].id
            return bestID
    """
