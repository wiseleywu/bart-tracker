#!/usr/bin/env python

from datetime import datetime, timedelta
from collections import OrderedDict
from bartTracker.api.utils import get_api_response
from bartTracker.api.keys import API_KEY


class StationSchedule(object):

    def __init__(self, date, sched_num, name, abbr, schedule):
        self.date = date
        self.sched_num = sched_num
        self.name = name
        self.abbr = abbr
        self.schedule = schedule

    def get_station_name(self):
        return (self.name, self.abbr)

    def get_schedule_date(self):
        return self.date

    def get_schedule_number(self):
        return self.sched_num

    def get_next_departure(self, now=None, station=None):
        if not now:
            now = datetime.now()
        if not station:
            indexes = [i for i,j in enumerate(self.schedule) if j > now]
        else:
            indexes = [i for i, (j,k) in enumerate(self.schedule.iteritems()) \
                       if j > now and k['trainHeadStation'] == station]
        if indexes:
            return self.schedule.items()[indexes[0]]


class LiveStationSchedule(object):

    def __init__(self, date, message, station, uri, time):
        self.date = date
        self.message = message
        self.orig = station.keys()
        self.uri = uri
        self.time = time


def get_station_schedule(orig, date):
    root = get_api_response(API_KEY, 'sched', 'stnsched', orig=orig, date=date)

    d = {}
    for key, value in enumerate(root):
        if value.tag  == 'station':
            d[value.tag] = value
        else:
            d[value.tag] = value.text

    schedule = OrderedDict()
    for key, value in enumerate(d['station']):
        if value.tag == 'abbr':
            d['abbr'] = value.text
        elif value.tag == 'name':
            d['name'] = value.text
        else:
            index_time = datetime.strptime(' '.join([d['date'], value.attrib['origTime']]), '%m/%d/%Y %I:%M %p')
            if 0 <= index_time.hour <= 2:
                index_time += timedelta(1)
            schedule[index_time] = value.attrib

    stn_schedule = StationSchedule(date = d['date'], sched_num= d['sched_num'],
                                   name = d['name'], abbr = d['abbr'],
                                   schedule = schedule)

    return stn_schedule


def get_all_live_stations_schedule():
    return get_live_station_schedule('ALL')


def get_live_station_schedule(orig):
    root = get_api_response(API_KEY, section='etd', command='etd', orig=orig)

    d = {}
    for key, value in enumerate(root):
        if value.tag  == 'station':
            if d.get(value.tag):
                d[value.tag].append(value)
            else:
                d[value.tag] = [value]
        else:
            d[value.tag] = value.text

    master = {}
    for station in d['station']:
        temp_d = {}
        for key, value in enumerate(station):
            if value.tag == 'etd':
                e = {}
                est = []
                for i, j in enumerate(value):
                    if j.tag == 'estimate':
                        est.append({i.tag: i.text for i in j})
                    else:
                        e[j.tag] = j.text
                dest = e['abbreviation']
                e['estimate'] = est
                temp_d[dest] = e
            else:
                temp_d[value.tag] = value.text
        master[temp_d['abbr']] = temp_d
    d['station'] = master

    return d