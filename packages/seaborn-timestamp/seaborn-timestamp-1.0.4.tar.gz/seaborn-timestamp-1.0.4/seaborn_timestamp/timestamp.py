__author__ = 'Ben Christenson'
__date__ = "9/21/15"

from datetime import *

import psycopg2

TIMESTAMP_FORMAT = '[0-9]{4}-[0-9]{2}-[0-9]{2}_[0-9]{2}' \
                   ':[0-9]{2}:[0-9]?[0-9.]{1,4}'
DEFAULT_TIMEZONE = -5
DEFAULT_TIMEZONE_AWARE = False


class Timestamp:
    STR_FORMAT = '%Y-%m-%d_%H:%M:%S.fff'

    def __init__(self, string_value=None,
                 datetime_value=None, str_format=None):
        self.str_format = str_format or self.STR_FORMAT
        self.value = string_value or datetime_to_str(
            datetime_value, self.str_format)

    @property
    def datetime(self):
        return str_to_datetime(self.value, self.str_format)


def set_timezone_aware(enable):
    global DEFAULT_TIMEZONE_AWARE
    DEFAULT_TIMEZONE_AWARE = enable


def cst_now():
    """
        This will return a datetime of utcnow - 6 hours for
        Central Standard Time
    :return: Datetime
    """
    try:
        ret = datetime.utcnow() + timedelta(hours=DEFAULT_TIMEZONE)
        if DEFAULT_TIMEZONE_AWARE:
            ret = ret.replace(
                tzinfo=psycopg2.tz.FixedOffsetTimezone(
                    name=None, offset=DEFAULT_TIMEZONE * 60))
        return ret
    except Exception as ex:
        return datetime.utcnow() + timedelta(hours=DEFAULT_TIMEZONE)


def today(date_time=None):
    """
        This will return a datetime of cst_now - 5 hours with only
        Year, Month, and Day
    :return:  Datetime
    """
    ret = date_time or cst_now()
    try:
        ret = datetime(year=ret.year, month=ret.month, day=ret.day)
        if DEFAULT_TIMEZONE_AWARE:
            ret = ret.replace(
                tzinfo=psycopg2.tz.FixedOffsetTimezone(
                    name=None, offset=DEFAULT_TIMEZONE * 60))
    except Exception as ex:
        pass
    return ret


def now(years=0, days=0, hours=0, minutes=0, seconds=0):
    """
    :param years:   int delta of years from now
    :param days:    int delta of days from now
    :param hours:   int delta of hours from now
    :param minutes: int delta of minutes from now
    :param seconds: float delta of seconds from now
    :return:        str of the now timestamp
    """
    date_time = datetime.utcnow()
    date_time += timedelta(days=days + years * 365, hours=hours,
                           minutes=minutes, seconds=seconds)
    return datetime_to_str(date_time)


def add_to_timestamp(timestamp, time_delta,
                     str_format='%Y-%m-%d_%H:%M:%S.fff'):
    """
        This will convert the timestamp to datetime, add the timedelta
        and then return it as a timestamp
    :param timestamp:    str of the date and time
    :param time_delta:   datetime.timedelta of the time to add
    :param str_format:   str of the format of the timestamp
    :return:             str of the new timestamp
    """
    date_time = str_to_datetime(timestamp, str_format) + time_delta
    return datetime_to_str(timestamp, str_format)


def datetime_to_str(date_time=None, str_format='%Y-%m-%d_%H:%M:%S.fff'):
    """
    :param   date_time: datetime of the date to convert to string
    :param   str_format: str of the format to return the string in
    :return: str of the timestamp
    """
    date_time = date_time or cst_now()
    if DEFAULT_TIMEZONE_AWARE:
        date_time += timedelta(hours=DEFAULT_TIMEZONE)
    ret = date_time.strftime(str_format.split('.f')[0])
    if '.f' in str_format:
        sig_digits = len(str_format.split('.')[-1]) + 1
        ret += str(date_time.microsecond % 1000 / 1000.0
                   )[1:].ljust(sig_digits, '0')[:sig_digits]
    return ret


def str_to_datetime(timestamp, str_format='%Y-%m-%d_%H:%M:%S.fff'):
    """
    :param str_format:
    :param timestamp: str of the timestamp
    :return:          datetime
    """
    date_time = datetime.strptime(timestamp.split('.')[0],
                                  str_format.split('.')[0])
    if '.' in timestamp:
        date_time += timedelta(seconds=eval('0.%s' % timestamp.split('.')[1]))
    if DEFAULT_TIMEZONE_AWARE:
        date_time = date_time.replace(
            tzinfo=psycopg2.tz.FixedOffsetTimezone(
                offset=DEFAULT_TIMEZONE * 60, name=None))
    return date_time


def next_day_of_month(day, date=None):
    date = date or cst_now()
    date += timedelta(days=(date.day < 7 and 31 or 27))
    ret = datetime(date.year, date.month, day)
    try:
        if DEFAULT_TIMEZONE_AWARE:
            ret = ret.replace(
                tzinfo=psycopg2.tz.FixedOffsetTimezone(
                    name=None, offset=DEFAULT_TIMEZONE * 60))
        return ret
    except Exception as ex:
        return datetime.utcnow() + timedelta(hours=DEFAULT_TIMEZONE)


def reformat_date(dt,
                  new_format='%Y-%m-%d_%H:%M:%S',
                  old_format='%Y%m%d%H%M%S.fff'):
    try:
        if dt == '':
            return dt
        if isinstance(dt, basestring):
            dt = str_to_datetime(dt, old_format)
        elif isinstance(dt, float):
            dt = time.localtime(dt) # todo review this
        return datetime_to_str(dt, new_format)
    except Exception as ex:
        return str(dt)
