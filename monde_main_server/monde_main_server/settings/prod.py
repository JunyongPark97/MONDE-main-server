import datetime
import os, sys
import requests
from .base import *

DEBUG = False

########## HOST CONFIGURATION
ALLOWED_HOSTS = [
    'monde-dev.ap-northeast-2.elasticbeanstalk.com',
    '15.164.101.147',
]

# https://www.vincit.fi/en/blog/deploying-django-elastic-beanstalk-https-redirects-functional-health-checks/
if os.getenv('SERVER_SOFTWARE', '').startswith('ElasticBeanstalk'):
    from django.core.exceptions import ImproperlyConfigured
    try:
        def get_ec2_hostname():
            ipconfig = 'http://169.254.169.254/latest/meta-data/local-ipv4'
            return requests.get(ipconfig, timeout=10).text
        ALLOWED_HOSTS.append(get_ec2_hostname())
    except:
        raise ImproperlyConfigured("You have to be running on AWS to use AWS settings")
########## END HOST CONFIGURATION

SECRET_KEY = load_credential("SECRET_KEY", "")


# AWS_REGION = 'ap-northeast-2'
# AWS_STORAGE_BUCKET_NAME = 'monde-server-storages'
# AWS_QUERYSTRING_AUTH = False
# AWS_S3_HOST = 's3.%s.amazonaws.com' % AWS_REGION
AWS_ACCESS_KEY_ID = load_credential('PROD_AWS_ACCESS_KEY_ID', "")
AWS_SECRET_ACCESS_KEY = load_credential('PROD_AWS_SECRET_ACCESS_KEY', "")
# AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
# AWS_S3_SECURE_URLS = True  # https

# Static Setting
# STATICFILES_LOCATION = 'static'
STATIC_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, STATICFILES_LOCATION)
# STATICFILES_STORAGE = 'monde_main_server.storages.StaticStorage'

# Media Setting
# MEDIAFIELS_LOCATION = 'media'
# MEDIA_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, MEDIAFIELS_LOCATION)
# MEDIAFILES_LOCATION = 'media'
# DEFAULT_FILE_STORAGE = 'monde_main_server.storages.MediaStorage'
