import googlemaps
from .settings import EUCLID_SCHEDULE_SETTINGS
from .models import BaseSchedule, DriverSchedule, RiderSchedule

def origin_lonlat(schedule : BaseSchedule):
    return (BaseSchedule.origin_lon, BaseSchedule.origin_lat)

def dest_lonlat(schedule : BaseSchedule):
    return (BaseSchedule.destination_lon, BaseSchedule.destination_lat)


class Pool(object):

    def __init__(self, driverschedule : DriverSchedule):
        self.driverschedule = driverschedule
        self.rideschedules = []

    def count_empty_seats(self):
        return self.driverschedule.car_capacity - len(self.rideschedules)

    def has_empty_seats(self):
        return self.count_empty_seats() == 0

    def add_rider(self, riderschedule):
        if not self.has_empty_seats() or not self.check_rider_compatibility(riderschedule):
            return False
        self.rideschedules.append(riderschedule)

    def check_rider_compatibility(self, riderschedule):
        return True

class DistanceMatrix(object):

    def __init__(self):
        self.coords = []
        self.gclient = googlemaps.Client()
        self.mat = []

    def add_coord(self, coord):
        if not self.coords:
            self.mat.append()

    def compute_one_to_all(self, coord):
        gc = googlemaps.Client(key=EUCLID_SCHEDULE_SETTINGS["GOOGLE_MAPS_API_KEY"])
        gcresult = gc.distance_matrix(
            origins = [coord],
            destinations = self.coords,
            mode = "driving"
        )

        for element in gcresult['rows'][0]["elements"]:
            duration = int(element['duration']["value"])
            distance = int(element['distance']["value"])



def has_time_window_overlap(ws1, we1, ws2, we2) -> bool:
    '''
    Compute if two timewindow overlap
    :param ws1: time window 1 start time
    :param we1: time window 1 end time
    :param ws2: time window 2 start time
    :param we2: time window 2 end time
    :return: True if the two time window has overlap, False otherwise
    '''
    latest_start = max(ws1, ws2)
    earliest_end = min(we1, we2)
    delta = earliest_end - latest_start
    if delta > 0:
        return True
    else:
        return False

def get_complete_distance_matrix(locations, departure_time=None):
    gclient = googlemaps.Client(key=EUCLID_SCHEDULE_SETTINGS["GOOGLE_MAPS_API_KEY"])
    query_result = gclient.distance_matrix(
        origins = locations,
        destinations = locations,
        mode = "driving",
        departure_time=departure_time
    )
