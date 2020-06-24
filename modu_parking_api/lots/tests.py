# from django.db import models
# from django.contrib.gis.db import models as db_models
# from django.contrib.auth import get_user_model
# from model_bakery import baker
# from rest_framework import status
# from rest_framework.authtoken.models import Token
# from rest_framework.test import APITestCase, CoreAPIClient
#
# # User = get_user_model()
# # from lots.models import Lot
from rest_framework import status
from rest_framework.test import APITestCase
from lots.models import Lot
from rest_framework.test import APIRequestFactory

"""Nothing"""


class LotsTestCase(APITestCase):
    def test_create(self):
        data = {
            "name": '성수 주차장 1번지',
            "address": '성수동 1번지',
            "latitude": '127.77',
            "longitude": '352.123',
            "basic_rate": '10000 ',
            "additional_rate": '6000',
            "partnership": False,
            "section_count": '1'
        }
        response = self.client.post('/api/lots/', data=data)
        self.assertTrue(response.data.get('name'))
        self.assertEqual(response.data.get('latitude'), data['latitude'])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.fail()

    def test_get(self):
        response = self.client.get(f'/api/lots/{self.lots[0].pk}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.users[0].username, response.data.get('username'))

    def test_update(self):
        data = {
            "name": '성수 주차장 2번지',
            "address": '성수동 2번지',
            "latitude": '127.79',
            "longitude": '352.129',
            "basic_rate": '20000 ',
            "additional_rate": '2000 ',
            "partnership": False,
            "section_count": '2'
        }
        response = self.client.patch(f'/api/users/{self.lots[0].pk}', data=data)
        # print('response >>>>>>', response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(self.lots[0].username, response.data.get('username'))

    def test_delete(self):
        response = self.client.delete(f'/api/lots/{self.lots[0].pk}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lots.objects.filter(pk=self.lots[0].id).count(), 0)
