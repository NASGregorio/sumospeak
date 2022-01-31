////////////////// AUXILIARY LOGIC //////////////////

+!preComputeRouteEdges([]).
+!preComputeRouteEdges([R|Routes]) <-
    !preComputeRouteEdges(Routes);
    .sumo_route_getEdges(R, Edges);
    +routeEdges(R, Edges).

+!enter_network(Route, Route) <-
    // Insert vehicle in sumo network (choose fastest route from beliefs)
    .my_name(X);
    .sumo_vehicle_add(X, Route);

    // Register run start time
    .sumo_simulation_getTime(CurrentTime);
    -startRunTime(_);
    +startRunTime(CurrentTime).

+!enter_network(Route, PreviousRoute) <-
    // Insert vehicle in sumo network (choose fastest route from beliefs)
    .my_name(X);
    .sumo_vehicle_add(X, Route);
    .sumo_vehicle_setColor(X, 255, 200, 0, 255);
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

+!incrementCurrentRoute(Route, RunCount) <-
    -routeRuns(Route, PreviousRun);
    RunCount = PreviousRun + 1;
    +routeRuns(Route, RunCount).
    


+!updateRouteAvg(1, Route, NewTime) <-
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
    +numberOfRuns(20);
    +currentRun(0);
    +routeRuns("routeShort", 0);
    +routeRuns("routeLong", 0);
    // Agent beliefs
    +maxAcceptableTravelTime(30);
    +routeRunTime("routeShort", 0, 31);
    +routeRunTime("routeLong", 0, 30);
    +routeTimeAvg("routeShort", 26);
    +routeTimeAvg("routeLong", 25).

///////////////////////// SUMOSPEAK PHASES /////////////////////////////////////

+!sumo_start <-
    !setupBeliefs;
    .sumo_route_getIDList(L);
    !preComputeRouteEdges(L);
    !getFastestRoute(NextRoute);
    !enter_network(NextRoute, NextRoute);
    .my_name(X);
    .sumo_vehicle_setColor(X, 0, 255, 0, 255).

+!sumo_arrival : currentRun(Curr) & numberOfRuns(Max) & Curr < Max - 1 <-

    // Register run time
    !getFastestRoute(LastRoute);
    //.print(",",LastRoute,",", Curr);

    !registerRunTime(LastRoute, RunTime);

    !incrementCurrentRoute(LastRoute, RunCount);

    !updateRouteAvg(RunCount, LastRoute, RunTime);
    routeTimeAvg("routeShort", RS);
    routeTimeAvg("routeLong", RL);
    
    // Do another run
    !getFastestRoute(NextRoute);
    !setupNextRun(NextRun);
    //.print("Run:", Curr, "|", LastRoute, RunTime, "sec | Avg Short:", RS, "| Avg Long:", RL);
    !enter_network(NextRoute, LastRoute).

+!sumo_arrival <-
    currentRun(Curr);
    !getFastestRoute(LastRoute);
    //.print(",",LastRoute,",", Curr);
    !registerRunTime(LastRoute, RunTime);
    !incrementCurrentRoute(LastRoute, RunCount);
    !updateRouteAvg(RunCount, LastRoute, RunTime);
    routeTimeAvg("routeShort", RS);
    routeTimeAvg("routeLong", RL);
    //.print("Run:", Curr, "|", LastRoute, RunTime, "sec | Avg Short:", RS, "| Avg Long:", RL);
    +runs_completed.