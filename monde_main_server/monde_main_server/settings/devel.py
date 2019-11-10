import datetime
import os, sys

from .base import *

DEBUG = True

ALLOWED_HOSTS = ['*']


INSTALLED_APPS += ('debug_toolbar',)

MIDDLEWARE = ['debug_toolbar.middleware.DebugToolbarMiddleware',] + MIDDLEWARE


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'monde',
        'HOST': 'choco-database.ckanfuynig82.ap-northeast-2.rds.amazonaws.com',
        'USER': load_credential("DEV_MONDE_DATABASE_USERNAME", ""),
        'PASSWORD': load_credential("DEV_MONDE_DATABASE_PASSWORD", ""),
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            }
    }
}

AWS_REGION = 'ap-northeast-2'
AWS_STORAGE_BUCKET_NAME = 'monde-server-storages'
AWS_QUERYSTRING_AUTH = False
AWS_S3_HOST = 's3.%s.amazonaws.com' % AWS_REGION
AWS_ACCESS_KEY_ID = load_credential('DEV_AWS_ACCESS_KEY_ID', "")
AWS_SECRET_ACCESS_KEY = load_credential('DEV_AWS_SECRET_ACCESS_KEY', "")
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_S3_SECURE_URLS = True  # https

# Static Setting
STATICFILES_LOCATION = 'static'
STATIC_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, STATICFILES_LOCATION)
STATICFILES_STORAGE = 'monde_main_server.storages.StaticStorage'

# Media Setting
MEDIAFIELS_LOCATION = 'media'
MEDIA_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, MEDIAFIELS_LOCATION)
MEDIAFILES_LOCATION = 'media'
DEFAULT_FILE_STORAGE = 'monde_main_server.storages.MediaStorage'
