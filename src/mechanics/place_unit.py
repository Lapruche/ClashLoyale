import pygame
import logging
from utils import log

class Cursor:

    def __init__(self,team):#camp=blue or red
        self.x=0
        self.y=0
        self.size=1
        self.color=(255,0,0)
        self.unit=None
        if team=="blue" or team=="red":
            self.team=team
            log.logger.send(f"Cursor {self} ", logging.DEBUG)
        else:
            log.logger.send(f"Could not load cursor {self}, camp didn't exist.", logging.ERROR)

    def cursor_move(self):
        L = pygame.key.get_pressed()
        L2 = []
        for key in range(len(L)):
            if L[key] != False:
                L2.append(pygame.key.name(L[key]))
        for i in range(len(L2)):
            if self.team=="blue":
                if L2[i] =="K_z":
                    self.y+=1
                if L2[i] =="K_q":
                    self.x-=1
                if L2[i] =="K_s":
                    self.y-=1
                if L2[i] =="K_d":
                    self.x+=1
            else:
                if L2[i] =="K_UP":
                    self.y+=1
                if L2[i] =="K_LEFT":
                    self.x-=1
                if L2[i] =="K_DOWN":
                    self.y-=1
                if L2[i] =="K_RIGHT":
                    self.x+=1

    def pick_up_unit(self,unit):
        self.pick_down_unit()
        self.unit=unit


    def pick_down_unit(self):
        if self.unit==None:
            log.logger.send(f"Zero utility,but if you want, why not... ", logging.DEBUG)
        self.unit=None

    def place_unit(self):
        pass




cursor1=Cursor("blue")
cursor2=Cursor("red")