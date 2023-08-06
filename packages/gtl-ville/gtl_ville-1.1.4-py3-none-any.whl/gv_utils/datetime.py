#!/usr/bin/env python3

from datetime import datetime

import pytz


LOCAL_TZ = pytz.timezone('Europe/Paris')
ISO_FORMAT = '%Y-%m-%dT%H:%M:%S%z'
HTTP_FORMAT = '%a, %d %b %Y %H:%M:%S GMT'


def now():
    return LOCAL_TZ.localize(datetime.now())


def utc():
    return LOCAL_TZ.localize(datetime.now()).astimezone(pytz.utc)


def to_utc(date):
    return date.astimezone(pytz.utc)


def to_string(date):
    return date.strftime(ISO_FORMAT)


def from_string(string, format=None):
    if format is None:
        format = ISO_FORMAT
    try:
        date = LOCAL_TZ.localize(datetime.strptime(string, format))
    except ValueError:
        date = datetime.strptime(string, format)
    return date


def to_http_date(date):
    return date.strftime(HTTP_FORMAT)
