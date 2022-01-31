+!sumo_start <-
    +run_network(3);
    !enter_network.

+!enter_network <-
    .my_name(X);
    !pick_random_route(Route);
    .print("Taking route:", Route);
    .sumo_vehicle_add(X, Route);

    run_network(Run);
    NRun = Run - 1;
    -run_network(Run);
    +run_network(NRun).

+!pick_random_route(Route) <-
    .sumo_route_getIDList(L);
    .length(L, Len);
    Len0 = Len - 1;
    .randint(0, Len0, RandInt);
    .nth(RandInt, L, Route).


+!sumo_arrival : run_network(0) <-
    .print("Route finished. All runs completed!");
    +runs_completed.

+!sumo_arrival : run_network(Run) <-
    run_network(Run);
    .print("Route finished. Starting next run...", Run);
    !enter_network.

+!sumo_close <-
    .print("Closing...").