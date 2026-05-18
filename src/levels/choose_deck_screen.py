import os

import pygame

import constant
from core import asset
from core.state import GameState
from levels.scene import Scene
from levels.widgets.button_widget import ButtonWidget
from utils import tracked_surface
from utils.scale_card import scale_card

deck_blue_selection = []


class ChooseDeckScreen(Scene):
    def __init__(self, modules):
        super().__init__(modules)  # Initializes the scene

        self.modules = modules
        self.ui = self.modules["ui"]
        self.state_manager = self.modules["state"]
        self.screen = self.ui.screen
        self.cartes = []

        self.ready_image = asset.get_image(constant.GUI_PATH / "ready.png").convert_alpha()
        self.ready_image = pygame.transform.scale(self.ready_image,
                                                  (constant.SCREEN_WIDTH / 5.7, constant.SCREEN_HEIGHT / 13))

        for file in os.listdir(constant.CARDS_PATH):
            if file.endswith(".png"):
                card = asset.get_image(constant.CARDS_PATH / file).convert_alpha()
                card = scale_card(card, 10.5, 9)
                self.cartes.append(tracked_surface.TrackedSurface(file, card))

    def start(self):
        super().start()

        x = 80
        y = 200

        components = [
            ButtonWidget(
                self.modules,
                (self.screen.get_width() / 1.5, self.screen.get_width() / 1.2),
                self.ready_image,
                lambda _: self.state_manager.set_state(GameState.GAME)
            )
        ]

        for carte in self.cartes:
            if x > self.screen.get_width() - 150:
                x = 80
                y += 130

            components.append(ButtonWidget(
                self.modules,
                (x, y),
                carte.surface,
                lambda widget: self.ajout_carte(widget),
                id=carte.name
            ))

            x += 120

        for component in components:
            self.ui.add_component(component)

        self.screen.blit(self.ready_image, (self.screen.get_width() / 1.5, self.screen.get_width() / 1.2))

        self.blue_choose_deck = asset.get_image(constant.GUI_PATH / "blue_choose_deck.png").convert_alpha()
        self.blue_choose_deck = pygame.transform.scale(self.blue_choose_deck,
                                                       (constant.SCREEN_WIDTH / 1.6, constant.SCREEN_HEIGHT / 28))
        self.ui.screen.blit(self.blue_choose_deck, (85, 80))

    def full_deck(self):
        return len(deck_blue_selection) == 8

    def run(self):
        super().run()

    def ajout_carte(self, widget):
        if widget.id in deck_blue_selection:
            print("carte pop")
            del deck_blue_selection[deck_blue_selection.index(widget.id)]
        else:
            if len(deck_blue_selection) < 8:
                print("carte add")
                deck_blue_selection.append(widget.id)
            else:
                print("deck full")
        print(deck_blue_selection)
