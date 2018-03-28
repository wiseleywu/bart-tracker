#!/usr/bin/env python

import requests
import xml.etree.ElementTree as ET


# global variable
SITE = 'http://api.bart.gov/api/'


def get_response(address):
    try:
        response = requests.get(address, timeout=10)
        response.raise_for_status()
    except requests.exceptions.Timeout:
        print 'Request Timeout. No information obtained'
        return
    except requests.exceptions.HTTPError as e:
        print e
        return
    if response.status_code == requests.codes.ok:
        return ET.fromstring(response.content)
    else:
        print "API Error! HTTP response code {} received".format(response.status_code)
        return


def get_api_response(api_key, section, command, **kwargs):
    # helper function
    def _param_to_request(key, value):
        return '{}={}'.format(key, value)

    arguments = []
    sect = section + '.aspx?'
    arguments.append(_param_to_request('cmd', command))
    arguments.append(_param_to_request('key', api_key))
    for key in kwargs:
        arguments.append(_param_to_request(key, kwargs[key]))

    address = SITE + sect + '&'.join(arguments)

    return get_response(address)

def get_element(element, key, attr=None):
    if key!=None and attr:
        return getattr(element[key], attr)
    elif key!=None and not attr:
        return element[key]
