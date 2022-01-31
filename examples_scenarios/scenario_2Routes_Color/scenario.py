from sumospeak.sumospeak import SumoSpeak
import time


############### DECLARE ASL AGENTS ################
aslAgents = [
	{"file":"agent.asl", "number":2000 }
]
###################################################

############# SETUP SIMULATION ##################
sim = SumoSpeak("example.sumocfg", True, True, aslAgents)

# SIMULATION LOOP CONDITION
def bdiAgentsStillHaveRuns():
	agents = sim.ASRunner.getAgents()
	for a in agents:
		if(not sim.ASRunner.testBelief(a, "runs_completed", ())):
			return True
	return False
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
start_time = time.time()
sim.run(bdiAgentsStillHaveRuns, 0)
print(time.time()- start_time)

# sim.start()
# while(networkHasVehicles()):
#     sim.step(0)
# sim.close()
###################################################
