from abc import ABC, abstractmethod

import pygame

import constant
from core import asset


class Scene(ABC):
    background_path = constant.GUI_PATH / "fond.png"

    def __init__(self, modules: dict):
        self.modules = modules
        self.ui = self.modules["ui"]
        self.background_image = None

    def load_background(self) -> None:
        if self.background_path is None:
            self.background_image = None
            return

        background_image = asset.get_image(self.background_path).convert_alpha()
        self.background_image = pygame.transform.scale(background_image,
                                                       (constant.SCREEN_WIDTH, constant.SCREEN_HEIGHT))

    def draw_background(self) -> None:
        if self.background_image is None:
            self.ui.screen.fill(constant.BACKGROUND_COLOR)
            return

        self.ui.screen.blit(self.background_image, (0, 0))

    @abstractmethod
    def start(self) -> None:
        """
        Runs once upon scene activation.
        """

        self.ui.clear_components()
        self.load_background()
        self.draw_background()

    @abstractmethod
    def run(self, dt=0) -> None:
        """
        Runs every frame upon scene activation
        """
        
        self.draw_background()
