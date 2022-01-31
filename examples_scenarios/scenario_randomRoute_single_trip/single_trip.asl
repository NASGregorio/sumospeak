+!sumo_start <-
    !enter_network.

+!enter_network <-
    .my_name(X);
    !pick_random_route(Route);
    .print("Taking route:", Route);
    .sumo_vehicle_add(X, Route).

+!pick_random_route(Route) <-
    .sumo_route_getIDList(L);
    .length(L, Len);
    Len0 = Len - 1;
    .randint(0, Len0, RandInt);
    .nth(RandInt, L, Route).

+!sumo_step <-
    .my_name(X);
    .sumo_vehicle_getRouteIndex(X, Idx).
    //.print(Idx).

+!sumo_arrival <-
    .print("Route finished!").

+!sumo_close <-
    .print("Closing...").