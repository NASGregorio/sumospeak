////////////////// AUXILIARY LOGIC //////////////////

+!preComputeRouteEdges([]).
+!preComputeRouteEdges([R|Routes]) <-
    !preComputeRouteEdges(Routes);
    .sumo_route_getEdges(R, Edges);
    +routeEdges(R, Edges).

+!enter_network <-
    // Insert vehicle in sumo network (choose fastest route from beliefs)
    !getFastestRoute(Route);
    .my_name(X);
    .print("Taking route:", Route);
    .sumo_vehicle_add(X, Route);

    // Register run start time
    .sumo_simulation_getTime(CurrentTime);
    -startRunTime(_);
    +startRunTime(CurrentTime).

+!getFastestRoute("routeShort") : routeTimeAvg("routeShort", L) & routeTimeAvg("routeLong", H) & L < H.
+!getFastestRoute("routeLong").

+!registerRunTime(Route, Diff) <-
    .sumo_simulation_getTime(CurrentTime);
    startRunTime(StartTime);
    Diff = CurrentTime - StartTime;
    currentRun(Run);
    +routeRunTime(Route, Run, Diff).

+!updateRouteAvg(0, Route, NewTime) <-
    -routeTimeAvg(Route, _);
    +routeTimeAvg(Route, NewTime).

+!updateRouteAvg(Run, Route, NewTime) <-
    -routeTimeAvg(Route, CurrentAvg);
    R1 = Run - 1;
    K = CurrentAvg * R1;
    Total = K + NewTime;
    Avg = Total/Run;
    +routeTimeAvg(Route, Avg).

+!setupNextRun(NextRum) <-
    -currentRun(LastRun);
    NextRum = LastRun + 1;
    +currentRun(NextRum).

+!setupBeliefs <-
    // Control beliefs
    +currentRun(0);

    // Agent beliefs
    +maxAcceptableTravelTime(30);
    +routeRunTime("routeShort", 0, 31);
    +routeRunTime("routeLong", 0, 30);
    +routeTimeAvg("routeShort", 31);
    +routeTimeAvg("routeLong", 30).

///////////////////////// SUMOSPEAK PHASES /////////////////////////////////////

+!sumo_start <-
    !setupBeliefs;
    .sumo_route_getIDList(L);
    !preComputeRouteEdges(L).

+!sumo_arrival <-

    // Register run time
    currentRun(Curr);
    !getFastestRoute(LastRoute);
    !registerRunTime(LastRoute, RunTime);
    !updateRouteAvg(Curr, LastRoute, RunTime);

    // Prepare for next run
    !setupNextRun(_);
    routeTimeAvg("routeShort", RS);
    routeTimeAvg("routeLong", RL);
    .print("Run:", Curr, "| Route finished in:", RunTime, "| Avg Short:", RS, "| Avg Long:", RL).