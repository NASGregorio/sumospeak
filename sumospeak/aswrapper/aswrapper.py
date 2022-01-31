from typing import List
import os

import agentspeak
import agentspeak.runtime
import agentspeak.ext_stdlib

class ASWrapper:
	def __init__(self, actions) -> None:
		self.__actions = actions
		self.__env = agentspeak.runtime.Environment()

	def addAgents(self, file: str, count: int) -> None:
		path = os.path.join(os.path.curdir, file)
		with open(path) as source:
			return self.__env.build_agents(source, count, self.__actions)


	def addBelief(self, agent: agentspeak.runtime.Agent, functor: str, args) -> None:
		agent.call(
			agentspeak.Trigger.addition,
			agentspeak.GoalType.belief,
			agentspeak.Literal(functor, args),
			agentspeak.runtime.Intention())

	def addAchievement(self, agent: agentspeak.runtime.Agent, functor: str, args) -> None:
		agent.call(
			agentspeak.Trigger.addition,
			agentspeak.GoalType.achievement,
			agentspeak.Literal(functor, args),
			agentspeak.runtime.Intention())
	
	def removeBelief(self, agent: agentspeak.runtime.Agent, functor: str, args) -> None:
		agent.call(
			agentspeak.Trigger.removal,
			agentspeak.GoalType.belief,
			agentspeak.Literal(functor, args),
			agentspeak.runtime.Intention())

	def testBelief(self, agent: agentspeak.runtime.Agent, functor: str, args) -> bool:
		return agent.test_belief(agentspeak.Literal(functor, args), agentspeak.runtime.Intention())

	def printAgent(self, agent: agentspeak.runtime.Agent):

		print("Belief base")
		for beliefs in agent.beliefs.values():
			for belief in beliefs:
				print("  ", agentspeak.asl_repr(belief))

		print("Rules")
		for rules in agent.rules.values():
			for rule in rules:
				print("  ", rule)

		print("Plans")
		for plans in agent.plans.values():
			for plan in plans:
				print("  ", "* %s%s%s : %s <- ... ." % (plan.trigger.value, plan.goal_type.value, plan.head, plan.context))

		print("Intentions")
		for i, intention_stack in enumerate(agent.intentions):
			for j, intention in enumerate(intention_stack):
				print("  ", i, j, intention.head_term, "("+agentspeak.asl_repr(intention.calling_term)+")")

	def testIntention(self, agent, intentionHead):
		for i, intention_stack in enumerate(agent.intentions):
			for j, intention in enumerate(intention_stack):
				if(intentionHead == agentspeak.asl_repr(intention.head_term)):
					return True
		return False

	def getAgent(self, name: str) -> agentspeak.runtime.Agent:
		return self.__env.agents[name]

	def getAgents(self) -> List[agentspeak.runtime.Agent]:
		return self.__env.agents.values()

	def runAgents(self, limit=None) -> None:
		for agent in self.__env.agents.values():
			if(limit is None):
				self.__env.run_agent(agent)
			else:
				[agent.step() for _ in range(limit)]

	def shuffleAgents(self) -> None:
		d_set = list(set(self.__env.agents))
		self.__env.agents = {i:self.__env.agents[i] for i in d_set}