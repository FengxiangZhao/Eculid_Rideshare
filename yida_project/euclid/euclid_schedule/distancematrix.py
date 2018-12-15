import time
import googlemaps

from utils.list import chunks

class QElement(object):
    '''
    The basic query element of a google map distance matrix query
    '''

    def __init__(self, origin, destination, metadata):
        self.origin = origin
        self.destination = destination
        self.status = metadata['status']
        self.duration = metadata['duration']['value']
        self.distance = metadata['duration']['value']

    def __str__(self):
        return "Distance Matrix Query Element from {:s} to {:s}. \nStatus:{:s}\nDuration:{:s}\nDistance:{:s}\n".format(
            str(self.origin),
            str(self.destination),
            self.status,
            str(self.duration),
            str(self.distance)
        )

class QRow(object):
    '''
    The basic query row of a google map distance matrix query
    '''
    def __init__(self):
        self.origin = None
        self.destinations = []
        self.elements = []

    def add_rowdata(self, origin, destinations, rowdata):
        if not self.origin and not self.destinations:
            self.origin = origin
            self.destinations = destinations
        elif not self.origin == origin:
            raise ValueError("Rowdata mismatch on origin")
        else:
            self.destinations.extend(destinations)
        for dest, element in zip(destinations, rowdata['elements']):
            self.elements.append(QElement(origin, dest, element))

    def add_elements(self, elements):
        self.elements.extend(elements)

    def get(self, index):
        return self.elements[index]

class QMatrix(object):
    '''
    The basic query matrix of a google map distance matrix query
    '''
    def __init__(self, api_key):
        self.api_key = api_key
        self.gclient = googlemaps.Client(key=api_key)
        self.locations = []
        self.rows = []

    def query(self, locations : list):
        '''
        Computes distance matrix for the full product for the locations given.
        Overcomes the goolge's 100 element per query limit and 1 second per 100 element query limit
        '''
        all_origins = []
        all_mat_rows = []
        for origins in chunks(locations, 10):
            mat_rows = [QRow() for _ in range(len(origins))]
            for destinations in chunks(locations, 10):
                # sleep for two seconds between each iteration of 100 elements
                time.sleep(2.)
                result = self.gclient.distance_matrix(origins, destinations, mode="driving")
                print('result obtained')
                for o, mat_row,result_row in zip(origins, mat_rows, result['rows']):
                    mat_row.add_rowdata(o, destinations, result_row)
            all_mat_rows.extend(mat_rows)
            all_origins.extend(origins)
        self.rows = all_mat_rows
        self.locations = all_origins

    def get_element(self, origin, destination):
        '''
        Obtain the element represents the query result from the origin to destination
        '''
        oindex = self.locations.index(origin)
        dindex = self.locations.index(destination)
        return self.rows[oindex].get(dindex)

