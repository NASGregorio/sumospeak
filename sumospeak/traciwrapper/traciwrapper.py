import os, sys
if 'SUMO_HOME' in os.environ:
	tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
	sys.path.append(tools)
else:
	sys.exit("please declare environment variable 'SUMO_HOME'")

from typing import List
import traci
from utils import CallbackList

SUMO_START = "sumo_start"
SUMO_STEP = "sumo_step"
SUMO_ARRIVAL = "sumo_arrival"
SUMO_CLOSE = "sumo_close"
SUMO_PHASE_LIST = [SUMO_START, SUMO_STEP, SUMO_ARRIVAL,SUMO_CLOSE]

class TraCIWrapper:
    def __init__(self, sumocmd: str) -> None:
        self.sumocmd = sumocmd
        self.cb_getArrivedIDList = CallbackList()
    
    def start(self) -> traci.Connection:
        traci.start(self.sumocmd)

    def step(self) -> None:
        traci.simulationStep()

        arrivals = traci.simulation.getArrivedIDList()
        if(len(arrivals) > 0):
            self.cb_getArrivedIDList.execute(arrivals)

    def close(self):
        traci.close(False)