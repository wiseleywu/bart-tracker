#!/usr/bin/env python

from sqlalchemy import Column, String, Integer, Date, Time, Float, DateTime
from base import Base


class Station(Base):
    __tablename__ = 'Bart stations'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    abbr = Column(String)
    gtfs_latitude = Column(Float)
    gtfs_longitude = Column(Float)
    address = Column(String)
    city = Column(String)
    county = Column(String)
    state = Column(String)
    zipcode = Column(Integer)

    def __init__(self, *initial_data, **kwargs):
        for dictionary in initial_data:
            for key in dictionary:
                setattr(self, key, dictionary[key])
        for key in kwargs:
            setattr(self, key, kwargs[key])


class TrainCount(Base):
    __tablename__ = 'Bart operating trains count'

    id = Column(Integer, primary_key=True)
    date = Column(Date)
    time = Column(Time)
    count = Column(Integer)
    msg = Column(String)

    def __init__(self, date, time, count, msg):
        self.date = date
        self.time = time
        self.count = count
        self.msg = msg


class Advisory(Base):
    __tablename__ = 'BART service advisory'

    id = Column(Integer, primary_key=True)
    posted = Column(DateTime)
    bsa_id = Column(Integer)
    station = Column(String)
    msg = Column(String)
    sms = Column(String)
    delay = Column(Integer)
    line = Column(String)
    direction = Column(String)
    issue = Column(String)


class Elevator(Base):
    __tablename__ = 'BART elevators outage'

    id = Column(Integer, primary_key=True)
    date = Column(Date)
    time = Column(Time)
    bsa_id = Column(Integer)
    equipment = Column(String)
    station = Column(String)
    msg = Column(String)
    sms = Column(String)
