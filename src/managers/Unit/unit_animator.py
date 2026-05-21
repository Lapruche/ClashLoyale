import logging

from core.animation import Animation
from utils import log


class UnitAnimator:
    def __init__(self):
        self._animations: dict[str, Animation] = {}
        self._current_animation = None

    def register_animation(self, name: str, animation: Animation):
        self._animations[name] = animation

    def play(self, name: str, force_check: bool = False):
        if name not in self._animations:
            log.logger.send("Tried to play an unavailable animation", logging.WARNING)
            return

        if name is not self._current_animation or force_check:
            self._current_animation = self._animations[name]
            self._current_animation.reset()

    def update(self, dt):
        if self._current_animation is not None:
            self._current_animation.update(dt)

    @property
    def current_sprite(self):
        if self._current_animation is not None:
            return self._current_animation.current_sprite
        return None
