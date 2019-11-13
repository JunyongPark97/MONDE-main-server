import datetime
import os, sys

from .base import *

DEBUG = True

ALLOWED_HOSTS = ['*']


INSTALLED_APPS += ('debug_toolbar',)

MIDDLEWARE = ['debug_toolbar.middleware.DebugToolbarMiddleware',] + MIDDLEWARE

DATABASES_DEV = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'monde',
        'HOST': load_credential("DATABASE_HOST", ""),
        'USER': load_credential("DEV_MONDE_DATABASE_USERNAME", ""),
        'PASSWORD': load_credential("DEV_MONDE_DATABASE_PASSWORD", ""),
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            }
    },
}

DATABASES.update(DATABASES_DEV)

INTERNAL_IPS = ('127.0.0.1',)

