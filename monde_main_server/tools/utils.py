import binascii
import datetime
import os
import pytz
import random

from django.utils import timezone


def get_random_md5():
    return binascii.hexlify(os.urandom(128))


def get_random_hex_string(digit):
    return binascii.hexlify(os.urandom(digit >> 1))


def get_date_from_today(**timedelta):
    today = timezone.now()
    return today - datetime.timedelta(**timedelta)


def get_local_time_now(tz):
    now = timezone.now()
    return now.astimezone(tz=tz)


def get_seoul_time_now():
    return get_local_time_now(pytz.timezone('Asia/Seoul'))


def create_random_string(length):
    c = 'abcdefghjkmnpqrstuvwsyz23456789'
    return ''.join(random.sample(c, length))
