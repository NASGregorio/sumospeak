from time import sleep
from abc import ABC, abstractmethod

from aswrapper import ASWrapper
from traciwrapper import TraCIWrapper, _traciactions, SUMO_START, SUMO_STEP, SUMO_ARRIVAL, SUMO_CLOSE, SUMO_PHASE_LIST
from utils import CallbackList

class SumoSpeak(ABC):

	def __init__(self, configPath: str, showGUI: bool, autoStartSimulation: bool, agents):
		self.__cb_simStep = CallbackList()
		self.__cb_simClose = CallbackList()
		self.__startAgentSpeak(agents)
		self.__startSumo(configPath, showGUI, autoStartSimulation)

		self.__traci.start()
		self.__traci.cb_getArrivedIDList.append(self.__fetchNewArrivals)

	def __startAgentSpeak(self, agents):
		self.ASRunner = ASWrapper(_traciactions.actions)

		self.__agentHooks = {
			SUMO_START: [],
			SUMO_STEP: [],
			SUMO_ARRIVAL: [],
			SUMO_CLOSE : []
		}

		for agent in agents:
			if(agent["number"] <= 0):
				raise RuntimeError("Number of agents must be 1 or higher")

			agents = self.ASRunner.addAgents(agent["file"], agent["number"])
			[self.__agentHooks[plan_key[2]].append(a) for a in agents for plan_key in a.plans.keys() if plan_key[2] in SUMO_PHASE_LIST]

	def __startSumo(self, configPath: str, showGUI: bool, autoStartSimulation: bool):
		cmd = ["sumo-gui" if showGUI else "sumo", "-c", configPath]
		if autoStartSimulation:
			cmd.append("--start")

		self.__traci = TraCIWrapper(cmd)

	def __fetchNewArrivals(self, arrivals):
		self.__arrivals = self.__arrivals + arrivals

		# Set arrival goal in agents that finished their route and have a plan for '.sumo_arrival'
		[self.ASRunner.addAchievement(newArrival, SUMO_ARRIVAL, ()) for newArrival in filter(lambda agent: agent.name in arrivals, self.__agentHooks[SUMO_ARRIVAL])]


	def onStepCB(self, cb):
		def wrapper():
			self.__cb_simStep.append(cb)
		return wrapper()

	def onCloseCB(self, cb):
		def wrapper():
			self.__cb_simClose.append(cb)
		return wrapper()

	def reset(self):
		self.__arrivals = ()

	def start(self) -> None:

		self.reset()

		# Set init goal in agents that have a plan for '.sumo_start'
		[self.ASRunner.addAchievement(agent, SUMO_START, ()) for agent in self.__agentHooks[SUMO_START]]
		self.ASRunner.runAgents()

	def step(self, stepDelay=0):
			self.__traci.step()

			# Set step goal in agents that are traveling and have a plan for '.sumo_step'
			[self.ASRunner.addAchievement(inTransit, SUMO_STEP, ()) for inTransit in filter(lambda agent: agent.name not in self.__arrivals, self.__agentHooks[SUMO_STEP])]
			self.ASRunner.runAgents()

			self.__cb_simStep.execute()
			
			sleep(stepDelay)

	def close(self):

		# Set close goal in agents that have a plan for '.sumo_close'
		[self.ASRunner.addAchievement(agent, SUMO_CLOSE, ()) for agent in self.__agentHooks[SUMO_CLOSE]]
		self.ASRunner.runAgents()

		self.__cb_simClose.execute()

		self.__traci.close()

	def run(self, loopClause, stepDelay=0) -> None:
		self.start()

		while loopClause():
			self.step(stepDelay)

		self.close()