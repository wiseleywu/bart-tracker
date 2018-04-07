#!/usr/bin/env python

from bartTracker.api.utils import get_api_response, get_element
from bartTracker.api.keys import API_KEY


class Station(object):
    def __init__(self, abbr, address, city, county, gtfs_latitude, gtfs_longitude, name, state, zipcode):
        self.abbr = abbr
        self.address = address
        self.city = city
        self.county = county
        self.gtfs_latitude = float(gtfs_latitude)
        self.gtfs_longitude = float(gtfs_longitude)
        self.name = name
        self.state = state
        self.zipcode = int(zipcode)

    def __str__(self):
        return 'Station Object: {}'.format(self.name)

    def get_station_name(self):
        return (self.name, self.abbr)

    def get_station_address(self):
        return ','.join([self.address, self.city, self.state, str(self.zipcode)])

    def get_station_county(self):
        return self.county

    def get_station_coordinate(self):
        return (self.gtfs_latitude, self.gtfs_longitude)

    def get_station_dict(self):
        return self.__dict__


def get_all_stations():
    return get_station('all')


def get_station(name):
    '''
    :return a specified station object with basic geographic inforamtion
    :param station: station abbreviation
    :return: station object
    '''
    root = get_api_response(API_KEY, 'stn', 'stns')

    keys = {}
    for i, j in enumerate(root):
        keys[j.tag] = i

    stations = get_element(root, keys.get('stations'))

    stn_keys = {}
    for i, j in enumerate(stations):
        stn_atr = {}
        for a, b in enumerate(j):
            stn_atr[b.tag] = a
        stn_keys[get_element(j, stn_atr.get('abbr'), attr='text')] = i

    if name.lower() == 'all':
        result = []
        for station in stations:
            stn = {c.tag: c.text for c in station}
            result.append(Station(abbr = stn.get('abbr'),
                          address = stn.get('address'),
                          city = stn.get('city'),
                          county = stn.get('county'),
                          gtfs_latitude = stn.get('gtfs_latitude'),
                          gtfs_longitude = stn.get('gtfs_longitude'),
                          name = stn.get('name'),
                          state = stn.get('state'),
                          zipcode = stn.get('zipcode')))
        return result
    else:
        req_stn = get_element(stations, stn_keys.get(name))
        if req_stn:
            stn = {c.tag: c.text for c in req_stn}
            return Station(abbr = stn.get('abbr'),
                           address = stn.get('address'),
                           city = stn.get('city'),
                           county = stn.get('county'),
                           gtfs_latitude = stn.get('gtfs_latitude'),
                           gtfs_longitude = stn.get('gtfs_longitude'),
                           name = stn.get('name'),
                           state = stn.get('state'),
                           zipcode = stn.get('zipcode'))
