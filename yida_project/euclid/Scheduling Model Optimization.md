### Scheduling Model Optimization

#### Present Model

- Origin and destination: stored as longitude and latitude
- Scheduled departure time window
- Driver only:
  - Car capacity
  - Driver time constraint

#### Objective

Define the system as the set of all participants, the matching algorithm should have the following two key objectives:

- Minimize system-wide vehicle-miles (M)
- Maximize the number of participants (P)

For M, the total distance for drivers should be minimized. That is, the similarity of routes should be considered as a key point when matching. A driver should take one (or more) riders that have similar routes altogether. The driver time constraint enforces this.

For P, the matching algorithm should be able to matching participants as much as possible. Although some matchings that maximizes P will not be optimal on the objective, the decision here is that P will have priority over optimality, as long as the time constraints are not exceeded.

#### Algorithm Sketch

To satisfy the above objective, we propose a greedy algorithm based on the time and distance.

```
Algorithm: Match-driver-with-riders
Description: Given a driver schedule and a list of rider schedule, find matching rider schedules that maximizes M and P.
Input: one driver schedule, N rider schedule
Initialization: N routes that starts from driver's origin and go to the rider's origin

While all the routes are not finished:
	For each of the routes:
		if the route not within time constraint:
			try finish up the route by putting the destinations to the route
			if the route cannot be finished within time constraint:
				remove the route
			else:
				mark the route finished
		else:
			insert another place to the route [from the destinations from the existing origins and the set of origins]

Return：the route that maximizes the P
```

The above algorithm works on a single driver schedule and a list of rider schedule. Therefore, it should be performed to all drivers and the list of riders that could be potentially matched with the driver. 