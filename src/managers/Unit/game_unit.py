import math

from constant import TRACE
from utils import log


class GameUnit:
    def __init__(self, camp: str, unit_id: int, properties: dict, pos: tuple):
        self.camp = camp
        self.properties = properties
        self.pos = [pos[0], pos[1]]
        self.id = unit_id
        self.health = self.properties["pv"]  # Current pv
        self.target = None

    def modify_health(self, amount):
        self.health = max(0, min(10, self.health + amount))
        log.logger.send(f"Unit {self.id} took {amount} damage.", TRACE)

    def on_spawn(self):
        pass

    def on_death(self):
        pass

    def target(self, units):
        
        pass

    def atk(self):
        if math.dist(self.pos, self.target) < self.properties["range"]:
            pass

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
            return bestID"""
