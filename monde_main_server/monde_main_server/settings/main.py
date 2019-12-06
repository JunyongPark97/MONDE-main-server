# coding: utf-8 


import os 

from monde_main_server.loader import load_credential

# os.environ : SETTINGS_MONDE=devel 로 설정되어있으면 devel
# https://stackoverflow.com/questions/10664244/django-how-to-manage-development-and-production-settings
# https://dayone.me/20Tcz1k
ENV_SETTINGS_MODE = (os.getenv('SETTINGS_MODE', 'devel'))
# if ENV_SETTINGS_MODE == 'prod':
#     from monde_main_server.settings.prod import *
# if ENV_SETTINGS_MODE == 'devel':
#     from monde_main_server.settings.devel import *
# if ENV_SETTINGS_MODE == '':
#     print('setting the SETTINGS_MODE')

# temp
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



# 기본적인 locale 에 대한 값을 설정한다.
SERVICE_LOCALE = os.getenv('SERVICE_LOCALE', None)
if not SERVICE_LOCALE:
    SERVICE_LOCALE = 'ko_KR'


if os.getenv('SERVER_SOFTWARE', '').startswith('ElasticBeanstalk'):
    # Running on Amazon Beanstalk
    # (EB configuration에는 "SERVER_SOFTWARE" 환경변수가 "ElasticBeanstalk"로 설정되어 있습니다.)
    # TODO: staging
    if ENV_SETTINGS_MODE == 'prod':
        from monde_main_server.settings.prod import *
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.mysql',
                'NAME': 'monde_prod',
                'HOST': load_credential("DATABASE_HOST", ""),
                'USER': load_credential("PROD_MONDE_DATABASE_USERNAME", ""),
                'PASSWORD': load_credential("PROD_MONDE_DATABASE_PASSWORD", ""),
                'OPTIONS': {
                    'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
                }
            },
        }
    elif ENV_SETTINGS_MODE == 'devel':
        from monde_main_server.settings.devel import *
        # Running in development, but want to access the staging SQL instance.
        DATABASES = {
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
else:
    # Not running on Amazon Beanstalk
    if ENV_SETTINGS_MODE == 'prod':
        from monde_main_server.settings.prod import *
        # Running in development, but want to access the production SQL instance.
        DATABASES = {
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
    elif ENV_SETTINGS_MODE == 'devel':
        from monde_main_server.settings.devel import *
        # Running in development, but want to access the staging SQL instance.
        DATABASES = {
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

# other database의 경우, deploy 위치에 상관없이 공통적으로 사용합니다.
DATABASES['mondebro'] = {
    'ENGINE': 'django.db.backends.mysql',
    'HOST': load_credential("DATABASE_HOST", ""),
    'NAME': 'mondebro',
    'USER': load_credential("MONDEBRO_DATABASE_USERNAME", ""),
    'PASSWORD': load_credential('MONDEBRO_DATABASE_PASSWORD', ""),
    'OPTIONS': {'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"}
}
DATABASES['mondebro'] = {
       'ENGINE': 'django.db.backends.mysql',
        'HOST': load_credential("DATABASE_HOST", ""),
        'NAME': 'web_crawler',
        'USER': load_credential("WEB_CRAWLER_DATABASE_USERNAME",""),
        'PASSWORD': load_credential('WEB_CRAWLER_DATABASE_PASSWORD'),
        'OPTIONS':{
            'init_command':"SET sql_mode='STRICT_TRANS_TABLES'",
            }
    }
