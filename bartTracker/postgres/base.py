#!/usr/bin/env python

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

USERNAME = os.environ['POSTGRES_USER']
PASSWORD = os.environ['POSTGRES_PASSWORD']
POSTGRES_DB = os.environ['POSTGRES_DB']
POSTGRES_PORT = os.environ['POSTGRES_PORT']

engine = create_engine('postgresql://{}:{}@localhost:{}/{}'.format(USERNAME, PASSWORD, POSTGRES_PORT, POSTGRES_DB))
Session = sessionmaker(bind=engine)

Base = declarative_base()
