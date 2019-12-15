import datetime
import os, sys
import requests
from .base import *

DEBUG = False

########## HOST CONFIGURATION
ALLOWED_HOSTS = [
    'monde-dev.ap-northeast-2.elasticbeanstalk.com',
    'monde-prod.ap-northeast-2.elasticbeanstalk.com',
    '15.164.101.147',
    '172.31.37.218'
    # '127.0.0.1'#temp
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


AWS_ACCESS_KEY_ID = load_credential('PROD_AWS_ACCESS_KEY_ID', "")
AWS_SECRET_ACCESS_KEY = load_credential('PROD_AWS_SECRET_ACCESS_KEY', "")
STATIC_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, STATICFILES_LOCATION)
