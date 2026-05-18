import pygame

from utils import tracked_surface


class ImageWidget:
    def __init__(self, modules: dict, pos: tuple, image: pygame.Surface | tracked_surface.TrackedSurface,
                 id: str | None = None) -> None:
        self.screen = modules["ui"].screen

        self.pos = pos
        self.id = id

        if type(image) == tracked_surface.TrackedSurface:
            self.image = image.surface
        else:
            self.image = image

    def handle_event(self, event: pygame.event.Event):
        pass

    def render(self):
        self.screen.blit(self.image, (self.pos[0], self.pos[1]))
