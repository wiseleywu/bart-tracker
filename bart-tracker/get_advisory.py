#!/usr/bin/env python

import requests
import xml.etree.ElementTree as ET
import os


API_KEY = os.environ['BART_API_KEY']
SITE = 'http://api.bart.gov/api/'
SECTION = ['bsa', 'etd', 'route', 'sched', 'stn', 'version']
SAVE_PATH = os.environ['SAVE_PATH']


def access_xml_element(element, key, attr=None):
    if key and attr:
        return getattr(element[key], attr)
    elif key and not attr:
        return element[key]

def get_advisory(bsa_type):
    response = requests.get(SITE + '{}.aspx?cmd={}&key={}'.format(bsa_type, 'bsa', API_KEY))

    if response.status_code == 200:
        root = ET.fromstring(response.content)

        keys = {}
        for i, j in enumerate(root):
            keys[j.tag] = i

        date = access_xml_element(root, keys.get('date'), attr='text')
        time = access_xml_element(root, keys.get('time'), attr='text')
        bsa = access_xml_element(root, keys.get('bsa'))
        bsa_id = bsa.attrib.get('id')

        bsa_keys = {}
        for i, j in enumerate(bsa):
            bsa_keys[j.tag] = i

        station = access_xml_element(bsa, bsa_keys.get('station'), attr='text')
        message = access_xml_element(bsa, bsa_keys.get('description'), attr='text')
        sms = access_xml_element(bsa, bsa_keys.get('sms_text'), attr='text')

        message = '"{}"'.format(message)
        sms = '"{}"'.format(sms)

        posted = access_xml_element(bsa, bsa_keys.get('posted'))

        return [date, time, bsa_id, station, message, sms, posted]

    else:
        print "API Error! HTTP response code {} received".format(response.status_code)

def get_train_count(bsa_type):
    response = requests.get(SITE + '{}.aspx?cmd={}&key={}'.format(bsa_type, 'count', API_KEY))
    if response.status_code == 200:
        root = ET.fromstring(response.content)
        keys = {}
        for i, j in enumerate(root):
            keys[j.tag] = i
        date = access_xml_element(root, keys.get('date'), attr='text')
        time = access_xml_element(root, keys.get('time'), attr='text')
        count = access_xml_element(root, keys.get('traincount'), attr='text')
        message = access_xml_element(root, keys.get('message'), attr='text')

        return [date, time, count, message]


    else:
        print "API Error! HTTP response code {} received".format(response.status_code)

bsa_response = get_advisory(SECTION[0])
bsa_response = ['None' if i is None else i for i in bsa_response]

count_response = get_train_count(SECTION[0])
count_response = ['None' if i is None else i for i in count_response]


with open(os.path.join(SAVE_PATH, 'advisory.txt'), 'a') as f:
    f.write(','.join(bsa_response)+'\n')

with open(os.path.join(SAVE_PATH, 'train_count.txt'),'a') as f:
    f.write(','.join(count_response)+'\n')