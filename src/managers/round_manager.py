import logging
from utils import log

class Round:
    def __init__(self,duree):#classe de round prenant une durée
        self.duree_init=duree
        self.duree=duree
        self.taux_elexir=1


    def timer_tick(self,dt):
        if 60<self.duree<60.1 and self.taux_elexir==1:
            self.taux_elexir+=1
        if self.duree>0.1:
            self.duree-=dt
        elif 0 < self.duree < 0.1:
            self.end_round()

    def convert_seconds_to_minutes(self):
        minutes, seconds = divmod(self.duree, 60)
        return minutes, seconds


    def end_round(self):
        log.logger.send("round is finished",logging.INFO)
        self.duree=-1

active_round: Round =None

def add_round(duree):
    global active_round
    active_round=Round(duree)
    print(active_round)




