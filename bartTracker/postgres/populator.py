#!/usr/bin/env python

from base import Session, engine, Base
from tables import Station, TrainCount, Advisory, Elevator
import bartTracker.api.stations as station_api

import os


# get env variables
elevator_txt = os.environ['ELEVATOR']
advisory_txt = os.environ['ADVISORY']
train_txt = os.environ['TRAIN']
API_KEY = os.environ['BART_API_KEY']
SITE = 'http://api.bart.gov/api/'

# generate database schema
Base.metadata.create_all(engine)

# create a new session
session = Session()

# populate station db
print "popluating Bart stations DB..."
stns_list = []
stns_dict = map(lambda x: x.get_station_dict(), station_api.get_all_stations())
for stn in stns_dict:
    stns_list.append(Station(stn))

# persists data
print "Adding to sessions...."
for stn in stns_list:
    session.add(stn)

# commit and close session
print "Committing session..."
session.commit()
print "Complete!"
session.close()
print "session closed"
