from math import *


class GameUnit:
    def __init__(self,camp,id,properties,X=0,Y=0):
        self.name=properties["name"]
        self.elixir_cost=properties["elixir_cost"]
        self.pv=properties["pv"]
        self.freq_atk=properties["freq_atk"]
        self.speed=properties["speed"]
        self.type=properties["type"]
        self.range=properties["range"]
        self.self_destruct=properties["self_destruct"]
        self.nb_unit=properties["nb_unit"]
        self.shield=properties["shield"]
        self.target=properties["target"]
        self.radius=properties["radius"]
        self.spawn_unit=properties["spawn_unit"]
        self.effect=properties["effect"]
        self.x=xcursor
        self.y=ycursor
        self.camp=camp
        self.id=id
    def spawn(xcursor,ycursor):
        pass

    def target():
        return None #demande à round manager

    def death():
        pass

    def distance(self,x1,y1):
        return sqrt((x1-self.x)**2+(y1-self.y)**2)

    def atk(self):
        if distance() < self.range:
            pass

    def pathfinding(self):
        dx = ennemi[0] - moi[0]
        dy = ennemi[1] - moi[1]
        radians = math.atan2(dy, dx)
        degres = math.degrees(radians)
        return degres

    def tageting(self):
        if self.camp=="rouge":
            bestID=None
            best_distance=100000
            cpt=0
            for unit in blue:
                cpt+=1
                if distance(blue[cpt].x,blue[cpt].y) < 1000:
                    if distance(blue[cpt].x,blue[cpt].y) < best_distance:
                        bestID=blue[cpt].id
            return bestID
        else:
            bestID=None
            best_distance=100000
            cpt=0
            for unit in red:
                cpt+=1
                if distance(red[cpt].x,red[cpt].y) < 1000:
                    if distance(red[cpt].x,red[cpt].y) < best_distance:
                        bestID=red[cpt].id
            return bestID

