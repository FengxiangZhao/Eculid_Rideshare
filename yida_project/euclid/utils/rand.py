import random
import string

def generate_random_string(N):
    '''
    generate random lowercase alphanumeric string of length N
    '''
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(N))


def generate_random_phone():
    '''
    generate random number of length 10 in place of a U.S. phone number
    '''
    return ''.join(random.choice(string.digits) for _ in range(10))

def generate_random_user_info():
    return {
        "username" : generate_random_string(5),
        "email" : generate_random_string(8) + '@gmail.com',
        "password" : generate_random_string(8),
        "phone" : generate_random_phone()
    }


def get_status_code_error_msg(expected, actual):
    return "Expected Status Code: {:d} \n Actual Status Code : {:d}".format(expected, actual)


###############################################
# Random geo location generator with U.S. Continents
# Modified from: https://github.com/michealbeatty/Random-Coords/blob/master/randomcoords.py
#
# US Geographic Information
#   Northernmost - (49.384472, -95.153389)
#   Southernmost - (24.433333, -81.918333)
#   Easternmost - (44.815278. -65.949722)
#   Westernmost - (48.164167. -124.733056)
#   Geographic Center - (39.833333. -98.583333)
###############################################

import googlemaps

US_NORTHERNMOST = 49.
US_SOUTHERNMOST = 25.
US_EASTERNMOST = -66.
US_WESTERNMOST = -124.

class BaseCoordinateValidator(object):

    def validate(self, latlng):
        raise NotImplementedError("Base class method not implemented")

class DefaultCoordinateValidator(BaseCoordinateValidator):
    def validate(self, latlng):
        return True

class GooglemapsValidator(BaseCoordinateValidator):

    def __init__(self, google_maps_api_key):
        self.gclient = googlemaps.Client(key=google_maps_api_key)

class CountryIsUSAValidator(GooglemapsValidator):

    def validate(self, latlng):
        result = self.gclient.reverse_geocode(latlng=latlng,
                                              result_type='country',
                                              language='en'
                                              )
        if not result:
            return False
        for address in result:
            name = address['address_components'][0]
            if not name['short_name'] == 'US':
                return False
        return True

class StateIsOhioValidator(GooglemapsValidator):

    def validate(self, latlng):
        result = self.gclient.reverse_geocode(latlng=latlng,
                                         result_type='administrative_area_level_1',
                                         language='en'
                                         )
        if not result:
            return False
        for address in result:
            name = address['address_components'][0]
            if not name['short_name'] == 'OH':
                return False
        return True

def generate_random_coordinates(
        n,
        precision=8,
        lat_range=(US_SOUTHERNMOST, US_NORTHERNMOST),
        lon_range=(US_EASTERNMOST, US_WESTERNMOST),
        coordinate_validator = DefaultCoordinateValidator()
):
    coordinate_list = []

    while len(coordinate_list) < n:
        lat = round(random.uniform(*lat_range), precision)
        lng = round(random.uniform(*lon_range), precision)
        if coordinate_validator.validate((lat,lng)):
            coordinate_list.append((lat,lng))
    return coordinate_list