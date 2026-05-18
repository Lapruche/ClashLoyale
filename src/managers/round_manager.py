
import time as t
from constant import TRACE
from utils import log

def round_manager():

    elexir_speed=1
    t_round = 180
    log.logger.send(f"Round begin!", TRACE)
    while t_round >=0:
        t1 = t.time()
        while t1-t2==0:
            t2=t.time()
        t_round -= 1
        if t_round >=60:
            elexir_speed += 1
    log.logger.send(f"Round end!", TRACE)
    log.logger.send(f"Time_add begin!", TRACE)
    t_round=120
    while t_round > 0:
        t1 = t.time()
        while t1-t2==0:
            t2=t.time()
        t_round -= 1
        if t_round>=60:
            elexir_speed += 1
    log.logger.send(f"Time_add end!", TRACE)
    log.logger.send(f"Mort_subite begin", TRACE)



