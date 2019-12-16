import datetime
import os, sys

from .base import *

DEBUG = True

ALLOWED_HOSTS = ['*']


INSTALLED_APPS += ('debug_toolbar',)

MIDDLEWARE = ['debug_toolbar.middleware.DebugToolbarMiddleware',] + MIDDLEWARE

INTERNAL_IPS = ('127.0.0.1', '15.164.101.147')

AWS_ACCESS_KEY_ID = load_credential('PROD_AWS_ACCESS_KEY_ID', "")
AWS_SECRET_ACCESS_KEY = load_credential('PROD_AWS_SECRET_ACCESS_KEY', "")
STATIC_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, STATICFILES_LOCATION)
