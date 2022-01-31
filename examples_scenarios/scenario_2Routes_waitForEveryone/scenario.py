from sumospeak.sumospeak import SumoSpeak
import traci

############### DECLARE ASL AGENTS ################
aslAgents = [
	{"file":"agent.asl", "number":10 }
]
###################################################

############# SETUP SIMULATION ##################
sim = SumoSpeak("network.sumocfg", True, True, aslAgents)

# SIMULATION LOOP CONDITION
def networkHasVehicles():
    return traci.simulation.getMinExpectedNumber() > 0
###################################################

########### DECLARE SIMULATION HOOKS ##############
# @sim.onStepCB
# def example_sim_step_cb():
#     print("STEP")

# @sim.onCloseCB
# def example_sim_end_cb():
#     print("onCloseCB")
###################################################

################ RUN SIMULATION ###################
sim.start()
sim.ASRunner.shuffleAgents()

for i in range(10):
	sim.reset()
	[sim.ASRunner.addAchievement(agent, "enter_network", ()) for agent in sim.ASRunner.getAgents()]
	sim.ASRunner.runAgents()

	while(networkHasVehicles()):
		sim.step(0.1)
	
sim.close()
###################################################