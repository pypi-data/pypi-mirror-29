#!/usr/bin/env python3

from datetime import datetime
import re

import pytz


LOCAL_TZ = pytz.timezone('Europe/Paris')
ISO_FORMAT_TZ = '%Y-%m-%dT%H:%M:%S%z'
ISO_FORMAT_MICRO_TZ = '%Y-%m-%dT%H:%M:%S.%f%z'
ISO_FORMAT = '%Y-%m-%dT%H:%M:%S'
ISO_FORMAT_MICRO = '%Y-%m-%dT%H:%M:%S.%f'
ISO_FORMATS = [ISO_FORMAT_TZ, ISO_FORMAT_MICRO_TZ, ISO_FORMAT, ISO_FORMAT_MICRO]
HTTP_FORMAT = '%a, %d %b %Y %H:%M:%S GMT'


def now():
    return LOCAL_TZ.localize(datetime.now().replace(microsecond=0))


def utc():
    return pytz.utc.localize(datetime.utcnow().replace(microsecond=0))


def to_tz(date, tz):
    if type(date) is not datetime:
        return None

    try:
        date = tz.localize(date)
    except ValueError:
        date = date.astimezone(tz)
    return date.replace(microsecond=0)


def to_utc(date):
    return to_tz(date, pytz.utc)


def to_local(date):
    return to_tz(date, LOCAL_TZ)


def to_string(date):
    if type(date) is str:
        return date
    if type(date) is not datetime:
        return None

    return date.strftime(ISO_FORMAT_TZ)


def from_string(string, dateformat=None):
    if type(string) is datetime:
        return to_local(string)
    if type(string) is not str:
        return None

    string = re.sub(r'([\+|\-][0-9]{2}):([0-9]{2})$', r'\1\2', string)
    dateformats = ISO_FORMATS
    if dateformat is not None:
        dateformats = [dateformat,] + dateformats

    for dateformat in dateformats:
        try:
            date = datetime.strptime(string, dateformat)
        except ValueError:
            pass
        else:
            return to_local(date)

    return None


def to_http_date(date):
    if type(date) is not datetime:
        return None

    return date.strftime(HTTP_FORMAT)
