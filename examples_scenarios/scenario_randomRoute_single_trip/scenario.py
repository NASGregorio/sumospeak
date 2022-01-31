from sumospeak.sumospeak import SumoSpeak
import traci

############### DECLARE ASL AGENTS ################
aslAgents = [
	{"file":"control_agent.asl", "number":1 },
	{"file":"single_trip.asl", "number":3 }
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

@sim.onCloseCB
def example_sim_end_cb():
    print("onCloseCB")
###################################################

################ RUN SIMULATION ###################
sim.run(networkHasVehicles, 0.1)
# sim.start()
# while(networkHasVehicles()):
#     sim.step(0.1)
# sim.close()
###################################################



#   mechanism for executing multiple runs

#   NOT POSSIBLE -> drop events/intentions is not implemented in agentspeak for python (exists in JASON)
#   second run mechanism that give "step" quota to each agent.
#       ie: traci step -> agent runs x steps -> traci step -> ...
#       possibily solves endless thinking/loop from agent speak side

#   maybe keep copy of agent list in aswrapper (3 lists - waiting, in transit, arrived)