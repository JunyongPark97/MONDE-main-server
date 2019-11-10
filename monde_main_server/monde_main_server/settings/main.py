# coding: utf-8 


import os 

from monde_main_server.loader import load_credential

# os.environ : SETTINGS_MONDE=devel 로 설정되어있으면 devel
# https://stackoverflow.com/questions/10664244/django-how-to-manage-development-and-production-settings
# https://dayone.me/20Tcz1k
ENV_SETTINGS_MODE = (os.getenv('SETTINGS_MODE', 'devel'))
print(ENV_SETTINGS_MODE)
# print(os.environ['TEST'])
if ENV_SETTINGS_MODE == 'prod':
    from monde_main_server.settings.prod import *
if ENV_SETTINGS_MODE == 'devel':
    from monde_main_server.settings.devel import *
if ENV_SETTINGS_MODE == '':
    print('setting the SETTINGS_MODE')


DATABASE_ROUTERS = [
    'monde_main_server.routers.MondeRouter'
]
