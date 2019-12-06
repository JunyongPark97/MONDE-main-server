import datetime
import os, sys

from .base import *

DEBUG = True

ALLOWED_HOSTS = ['*']


INSTALLED_APPS += ('debug_toolbar',)

MIDDLEWARE = ['debug_toolbar.middleware.DebugToolbarMiddleware',] + MIDDLEWARE

INTERNAL_IPS = ('127.0.0.1', '15.164.101.147')

