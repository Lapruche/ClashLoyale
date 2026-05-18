import logging
import sys
import traceback

import pygame

import constant
from core.game import Game
from core.scaling import auto_scaling
from utils import log


def run():
    log.Logger('debug.log', constant.TRACE)  # Will directly populate the logger variable

    # Pygame init
    pygame.init()
    pygame.font.init()

    game = Game()
    clock = pygame.time.Clock()

    log.logger.send("Clash Loyale is ready ! hehehehaw")
    auto_scaling()
    while game.running:
        dt = clock.tick(60) / 1000  # FPS
        events = pygame.event.get()

        game.tick(events, dt)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    try:
        run()
    except Exception:
        log.logger.send("----------------------CRITIQUES---------------------", logging.CRITICAL)
        log.logger.send("// I'm sorry, dave. I'm afraid I can't do that. HOG RIIIIDAAAAH\n", logging.CRITICAL)
        exc_type, exc_value, exc_traceback = sys.exc_info()
        tb_list = traceback.format_exception(exc_type, exc_value, exc_traceback)

        for line in tb_list:
            clean_line = line.replace("\n", "")
            log.logger.send(clean_line, logging.CRITICAL)

        log.logger.send("----------------------------------------------------\n", logging.CRITICAL)
        pygame.quit()
        sys.exit(-1)
