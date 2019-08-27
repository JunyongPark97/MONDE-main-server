from rest_framework import status
from rest_framework.test import APITestCase

from notices.models import Notice


class NoticeTestCase(APITestCase):
    def setUp(self):
        Notice.objects.create(title="title", content="content")

    def test_notice_list(self):
        response = self.client.get('/api/v2/notice/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

