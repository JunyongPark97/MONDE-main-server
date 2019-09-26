from django.utils.deconstruct import deconstructible

import uuid

import os

# See: https://code.djangoproject.com/ticket/22999#no1
@deconstructible
class GiveRandomFileName(object):
    def __init__(self, path):
        self.path = path

    def __call__(self, instance, filename):
        filename = filename.split('.')
        extension = filename[-1]
        filename = '{}.{}'.format(filename[0] + '_' + str(uuid.uuid4().hex), extension)
        return os.path.join(self.path, filename)
