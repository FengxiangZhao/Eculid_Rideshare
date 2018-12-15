from django.utils import timezone
from django.db.models import Q
from .settings import EUCLID_SCHEDULE_SETTINGS
from .models import BaseSchedule, DriverSchedule, RiderSchedule
from .distancematrix import QMatrix
from utils.time import has_time_window_overlap
import itertools

def perform_matching():
    '''
    Perform matching for the next period
    '''
    # obtain the set of drivers that are to be matched in the next period
    ds_queryset = DriverSchedule.objects.filter(
        is_cancelled=False,
        scheduled_departure_datetime__gt=timezone.now() + timezone.timedelta(hours=3),
    )

    for driver in ds_queryset:
        if driver.has_match or not driver.is_active:
            continue
        # filter a list of riders that has time overlap with the driver schedule
        riders = RiderSchedule.objects.filter(
            Q(is_cancelled=False),
            Q(
                    Q(scheduled_departure_datetime__lte=driver.scheduled_departure_datetime) &
                    Q(latest_arrival_datetime__gt=driver.scheduled_departure_datetime)
            ) | (
                    Q(scheduled_departure_datetime__gt=driver.scheduled_departure_datetime) &
                    Q(scheduled_departure_datetime__lt=driver.latest_arrival_datetime)
            ),
            Q(matching_driver__isnull=True)
        )
        if not riders:
            continue
        else:
            match(driver, list(riders))

def get_distance_matrix(schedules : [BaseSchedule]):

    locations = [l for s in schedules for ls in s.get_latlons() for l in ls]
    distance_matrix = QMatrix(getattr(EUCLID_SCHEDULE_SETTINGS, 'GOOGLE_MAPS_API_KEY'))
    distance_matrix.query(locations)
    return distance_matrix

def match(driver : DriverSchedule, riders : [RiderSchedule]):

    if not riders:
        return

    # construct an instance of the distance matrix
    orig_points = [ driver.origin_latlon ]
    orig_points += [r.origin_latlon for r in riders]
    dest_points = [driver.dest_latlon]
    dest_points += [r.dest_latlon for r in riders]
    distance_matrix = QMatrix(getattr(EUCLID_SCHEDULE_SETTINGS, 'GOOGLE_MAPS_API_KEY'))
    distance_matrix.query(orig_points + dest_points)
    del orig_points, dest_points

    combination_max_len = min(driver.car_capacity, 5, len(riders))

    for combination_len in range(combination_max_len, 0, -1):
        result = make_match(driver, riders, combination_len, distance_matrix)
        if result:
            for r in result:
                r.set_match_driver(driver)
            # TODO: fill in the template details / context
            driver.notify_user("matched", {})
            return


def make_match(driver : DriverSchedule,
                  riders : [RiderSchedule],
                  combination_target : int,
                  distance_matrix : QMatrix
                  ):

    driver_departure_time_window = driver.get_departure_time_window()
    driver_arrival_time_window = driver.get_arrival_time_window()
    # all the rider's time window is stored all at once to reduce query time
    rider_departure_time_windows_dict = {rider : rider.get_departure_time_window() for rider in riders}
    rider_arrival_time_windows_dict = {rider: rider.get_arrival_time_window() for rider in riders}

    def is_driver_compatible(route : []):
        complete_route_time_in_seconds = sum(
            [
                distance_matrix.get_element(route[i], route[i+1]) for i in range(len(route) - 1)
            ]
        )
        return has_time_window_overlap(
            driver_departure_time_window[0] + complete_route_time_in_seconds,
            driver_departure_time_window[1] + complete_route_time_in_seconds,
            driver_arrival_time_window[0],
            driver_arrival_time_window[1]
        )

    def is_rider_compatible(route : [], route_riders : (RiderSchedule,)):
        for rider in route_riders:

            # the estimated time spent in between driver's departure time and the rider is picked up
            rider_pickup_time_spent = \
                timezone.timedelta(
                    seconds=sum([
                        distance_matrix.get_element(route[i], route[i + 1]) for i in
                        range(route.index(rider.origin_latlon))
                    ])
                )

            # the time spent in between driver'departure time and the rider is dropped off
            rider_dropoff_time_spent = rider_pickup_time_spent + \
                                 timezone.timedelta(
                                     seconds=sum([distance_matrix.get_element(route[i], route[i + 1])
                                                  for i in range(route.index(rider.origin_latlon),
                                                                 route.index(rider.dest_latlon))
                                                  ])
                                 )

            rider_departure_time_window = rider_departure_time_windows_dict[rider]
            rider_arrival_time_window = rider_arrival_time_windows_dict[rider]
            actual_rider_departure_time_window = (driver_departure_time_window[0] + rider_pickup_time_spent,
                                                  driver_departure_time_window[1] + rider_pickup_time_spent)
            actual_rider_arrival_time_window = (driver_departure_time_window[0] + rider_dropoff_time_spent,
                                                driver_departure_time_window[1] + rider_dropoff_time_spent)

            if not has_time_window_overlap(
                actual_rider_departure_time_window[0],
                actual_rider_departure_time_window[1],
                rider_departure_time_window[0],
                rider_departure_time_window[1]
            ) or not has_time_window_overlap(
                actual_rider_arrival_time_window[0],
                actual_rider_arrival_time_window[1],
                rider_arrival_time_window[0],
                rider_arrival_time_window[1]
            ) :
                return False
        return True


    # check the combinations
    if len(riders) == combination_target:
        all_rider_combinations = [tuple(riders)]
    elif len(riders) > combination_target:
        all_rider_combinations = itertools.combinations(riders, combination_target)
    else:
        raise ValueError("The number of riders is smaller than the combination target")


    for rider_combination in all_rider_combinations:
        rider_locations = [p for rider in rider_combination for p in rider.get_latlons()]
        routes = itertools.permutations(rider_locations)

        for route in routes:
            # check if the origin of a point always comes before its corresponding destination
            is_route_valid = True
            for rider in rider_combination:
                if route.index(rider.origin_latlon) > route.index(rider.dest_latlon):
                    is_route_valid = False
                    break
            if not is_route_valid:
                continue

            # construct on the complete route
            route = list(route)
            route.insert(0, driver.origin_latlon)
            route.append(driver.dest_latlon)
            driver_is_compatible = is_driver_compatible(route)
            rider_is_compatible = is_rider_compatible(route, rider_combination)

            if not driver_is_compatible or not rider_is_compatible:
                continue
            else:
                return rider_combination
    return None