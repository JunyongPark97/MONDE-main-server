# coding: utf-8 


import json

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from versions.models import Version


class TestVersionAPI(APITestCase):
    
    def setUp(self):
        self.version = Version.objects.create(name='android', version=1000)

    def test_version_api(self):
        url = reverse('version:api:version-list')

        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(isinstance(data, list))
        self.assertIn('name' ,data[0])
        self.assertIn('version' ,data[0])
        self.assertEqual(data[0]['name'], 'android')
        self.assertEqual(data[0]['version'], 1000)
