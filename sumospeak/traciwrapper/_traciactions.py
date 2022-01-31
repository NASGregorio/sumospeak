from typing import Tuple
import agentspeak.ext_stdlib
import agentspeak

import os, sys
if 'SUMO_HOME' in os.environ:
	tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
	sys.path.append(tools)
else:
	sys.exit("please declare environment variable 'SUMO_HOME'")

import traci

actions = agentspeak.Actions(agentspeak.ext_stdlib.actions)

############### EDGE VALUE RETRIEVAL ################
@actions.add_function(".sumo_edge_getTraveltime", (str,))
def edge_getTraveltime(edgeID: str):
	return traci.edge.getTraveltime(edgeID)


############### LANE VALUE RETRIEVAL ################
@actions.add_function(".sumo_lane_getLastStepMeanSpeed", (agentspeak.Literal,))
def lane_getLastStepMeanSpeed(laneID: agentspeak.Literal):
	return traci.lane.getLastStepMeanSpeed(laneID.asl_repr())


############### ROUTE VALUE RETRIEVAL ################
@actions.add_function(".sumo_route_getIDList", ())
def route_getIDList():
	return traci.route.getIDList()

@actions.add_function(".sumo_route_getEdges", (str,))
def route_getEdges(routeID: str):
	return traci.route.getEdges(routeID)



############### SIMULATION VALUE RETRIEVAL ################
@actions.add_function(".sumo_simulation_getTime", ())
def simulation_getTime():
	return traci.simulation.getTime()


############### VEHICLE VALUE RETRIEVAL ################
@actions.add_procedure(".sumo_vehicle_add", (agentspeak.Literal,str,))
def vehicle_add(name: agentspeak.Literal, route):
	if(not name.is_atom()):
		print("Failed to add car for agent", name.asl_repr())
	traci.vehicle.add(name.functor, route)

@actions.add_function(".sumo_vehicle_getLaneID", (agentspeak.Literal,))
def vehicle_getLaneID(vehID: agentspeak.Literal):
	return traci.vehicle.getLaneID(vehID.asl_repr())

@actions.add_function(".sumo_vehicle_getRoadID", (agentspeak.Literal,))
def vehicle_getRoadID(vehID: agentspeak.Literal):
	return traci.vehicle.getRoadID(vehID.asl_repr())

@actions.add_function(".sumo_vehicle_getRouteIndex", (agentspeak.Literal,))
def vehicle_getRouteIndex(vehID: agentspeak.Literal):
	if(vehID in traci.vehicle.getIDList()):
		return traci.vehicle.getRouteIndex(vehID.asl_repr())

@actions.add_function(".sumo_vehicle_getSpeed", (agentspeak.Literal,))
def vehicle_getSpeed(vehID: agentspeak.Literal):
	return traci.vehicle.getSpeed(vehID.asl_repr())
		
@actions.add_procedure(".sumo_vehicle_setColor", (agentspeak.Literal, int, int, int, int))
def vehicle_setColor(vehID: agentspeak.Literal, colorR: int, colorG: int, colorB: int, colorA: int):
	traci.vehicle.setColor(vehID.asl_repr(), (colorR, colorG, colorB, colorA))