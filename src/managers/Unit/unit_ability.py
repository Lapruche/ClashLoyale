class UnitAbility:
    def __init__(self, name: str, cooldown: float):
        self.name: str = name
        self.cooldown: float = cooldown
        self._timer: float = cooldown

    def is_ready(self) -> bool:
        return self._timer <= 0

    def execute(self, caster, target) -> None:
        raise NotImplemented

    def update(self, dt):
        self._timer = max(0, self._timer - dt)
