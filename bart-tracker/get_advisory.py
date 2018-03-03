#!/usr/bin/env python

import requests
import xml.etree.ElementTree as ET
import os
import sys


API_KEY = os.environ['BART_API_KEY']
SITE = 'http://api.bart.gov/api/'
SECTION = ['bsa', 'etd', 'route', 'sched', 'stn', 'version']
SAVE_PATH = os.environ['SAVE_PATH']


def access_xml_element(element, key, attr=None):
    if key!=None and attr:
        return getattr(element[key], attr)
    elif key!=None and not attr:
        return element[key]

def get_advisory(bsa_type, debug=False):
    api_location = SITE + '{}.aspx?cmd={}&key={}'.format(bsa_type, 'bsa', API_KEY)
    try:
        response = requests.get(api_location, timeout=10)
        response.raise_for_status()
    except requests.exceptions.Timeout:
        sys.exit('Request Timeout. No information obtained')
    except requests.exceptions.HTTPError as e:
        sys.exit(e)

    if response.status_code == requests.codes.ok:
        root = ET.fromstring(response.content)

        msg = []
        for child in root.iter():
            child.text and msg.append(child.text.lower())
        if 'invalid key' in msg:
            sys.exit('Error found in response: {}'.format(','.join(msg)))

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

        if debug:
            return response
        else:
            return [date, time, bsa_id, station, message, sms, posted]
    else:
        sys.exit("API Error! HTTP response code {} received".format(response.status_code))

def get_train_count(bsa_type, debug=False):
    response = requests.get(SITE + '{}.aspx?cmd={}&key={}'.format(bsa_type, 'count', API_KEY))
    if response.status_code == requests.codes.ok:
        root = ET.fromstring(response.content)
        keys = {}
        for i, j in enumerate(root):
            keys[j.tag] = i
        date = access_xml_element(root, keys.get('date'), attr='text')
        time = access_xml_element(root, keys.get('time'), attr='text')
        count = access_xml_element(root, keys.get('traincount'), attr='text')
        message = access_xml_element(root, keys.get('message'), attr='text')

        if debug:
            return response
        else:
            return [date, time, count, message]
    else:
        sys.exit("API Error! HTTP response code {} received".format(response.status_code))

def get_elevator_outage(bsa_type, debug=False):
    response = requests.get(SITE + '{}.aspx?cmd={}&key={}'.format(bsa_type, 'elev', API_KEY))
    if response.status_code == requests.codes.ok:
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
        equipment_type = access_xml_element(bsa, bsa_keys.get('type'), attr='text')
        station = access_xml_element(bsa, bsa_keys.get('station'), attr='text')
        message = access_xml_element(bsa, bsa_keys.get('description'), attr='text')
        sms = access_xml_element(bsa, bsa_keys.get('sms_text'), attr='text')

        message = '"{}"'.format(message)
        sms = '"{}"'.format(sms)

        if debug:
            return root
        else:
            return [date, time, bsa_id, equipment_type, station, message, sms]

elev_response = get_elevator_outage(SECTION[0])
elev_response = ['None' if i is None else i for i in elev_response]

bsa_response = get_advisory(SECTION[0])
bsa_response = ['None' if i is None else i for i in bsa_response]

count_response = get_train_count(SECTION[0])
count_response = ['None' if i is None else i for i in count_response]


with open(os.path.join(SAVE_PATH, 'advisory.txt'), 'a') as f:
    f.write(','.join(bsa_response)+'\n')

with open(os.path.join(SAVE_PATH, 'train_count.txt'),'a') as f:
    f.write(','.join(count_response)+'\n')

with open(os.path.join(SAVE_PATH, 'elevator_status.txt'),'a') as f:
    f.write(','.join(elev_response)+'\n')