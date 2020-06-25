<<<<<<< HEAD
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
from django.urls import reverse
from model_bakery import baker
from rest_framework import status, response
from rest_framework.test import APITestCase
from lots.models import Lot
from lots.views import LotsViewSet

"""Nothing"""


class LotsTestCase(APITestCase):
    def setUp(self) -> None:
        # 얘는 묶음
        self.lots = baker.make(Lot, _quantity=3)
        # 얜 하나
        # self.lot = Lot(
        #     name="성수 주차장 2번지",
        #     address="Dont Know",
        #     phone_num="010-4451-2211",
        #     latitude=127.12,
        #     longitude=352.123,
        #     basic_rate=20000,
        #     additional_rate=2000,
        #     partnership=False,
        #     section_count=3,
        # )
        # self.lot = Lot.objects.create(
        #                               name="IDONTHAVEANAME",
        #                               address="Dont Know",
        #                               phone_num="010-4451-2211",
        #                               latitude=127.12,
        #                               longitude=352.123,
        #                               basic_rate=20000,
        #                               additional_rate=2000,
        #                               partnership=False,
        #                               section_count=3,)
        print(self.lots[0].pk)

    def test_create(self):
        data = {
            "name": '성수 주차장 1번지',
            "address": '성수동 1번지',
            "latitude": 127.77,
            "longitude": 352.123,
            "phone_num": '010-1111-2222',
            "basic_rate": 10000,
            "additional_rate": 6000,
            "partnership": False,
            "section_count": 1
        }
        response = self.client.post('/api/lots', data=data)
        self.assertTrue(response.data.get('name'))
        self.assertEqual(response.data.get('latitude'), data["latitude"])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_retrieve(self):
        # 권한을 주지 않아서 아직 사용하지 않습니다. 하게 된다면 유저를 생성하고, 사용하시면 됩니다.
        response = self.client.get(f'/api/lots/{self.lots[0].pk}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.lots[0].name, response.data.get('name'))


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
        response = self.client.patch(f'/api/lots/{self.lots[0].pk}', data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(Lot.name, response.data.get('name'))

    # def test_delete(self):
    #     response = self.client.delete(f'/api/users/{self.lot.pk}')
    #     self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    #     self.assertEqual(User.objects.filter(pk=self.users[0].id).count(), 0)
    def test_delete(self):
        response = self.client.delete(f'api/lots/{self.lots[0].pk}')
        # response = self.client.delete(f'/api/users/{self.users[0].pk}')
        # url = reverse(f'/api/lots/{self.lot}', kwargs={'pk': self.lot.pk})
        # self.client.delete(url)
        # self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # self.assertEqual(self.lots[0].filter(pk=self.lots[0].pk.count(), 2))
        self.assertEqual(Lot.objects.filter(pk=self.lots[0].id).count(), 1)

    # def test_should_delete(self):
    #     response = self.client.delete(f'/api/users/{self.users[0].pk}')
    #     self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    #     self.assertEqual(User.objects.filter(pk=self.users[0].id).count(), 0)

    # def test_should_delete(self):
    #     response = self.client.delete(f'/api/users/{self.users[0].pk}')
    #     self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    #     self.assertEqual(User.objects.filter(pk=self.users[0].id).count(), 0)
    # response = self.client.post('/api/lots', data=data)
#         print('resopnse >>>>', response)
#         self.assertTrue(response.data.get('name'))
#         self.assertEqual(response.data.get('latitude'), data["latitude"])
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
=======
from random import *

from rest_framework.test import APITestCase
from lots.models import Lot
from haversine import haversine


class LotsTestCase(APITestCase):

    def setUp(self) -> None:

        self.zoom_lv = 2

        lat_min = 37.537
        lat_max = 37.587
        lng_min = 126.951
        lng_max = 127.036

        rate_min = 10
        rate_max = 50

        # create lots with random location and basic_rate
        for i in range(500):
            rate = randint(rate_min, rate_max) * 1000   # return integer
            lat = uniform(lat_min, lat_max)             # return float
            lng = uniform(lng_min, lng_max)
            Lot.objects.create(latitude=lat, longitude=lng, name=f'{i}lot', basic_rate=rate)

        # user coordinate
        self.lat = uniform(lat_min, lat_max)
        self.lng = uniform(lng_min, lng_max)

        # data for request body
        self.user_data = {
            'latitude': self.lat,
            'longitude': self.lng,
        }
        # data for haversine method
        self.user_location = (self.lat, self.lng)

    def test_map_list(self):
        user_location = {
            'latitude': self.lat,
            'longitude': self.lng,
            'zoom_lv': 2  # In order to retrieve lots within 2km
        }
        response = self.client.get('/api/lots/map', data=user_location)
        self.assertEqual(response.status_code, 200)

        user_location = (self.lat, self.lng)
        for lot in response.data:
            lat = lot['latitude']
            lng = lot['longitude']
            lot_location = (lat, lng)

            distance = haversine(lot_location, user_location)
            print(distance)
            self.assertLessEqual(distance, 2)  # distance between user and lot should be within 2km

    def test_distance_odr_list(self):
        response = self.client.get('/api/lots/distance_odr', data=self.user_data)
        self.assertEqual(response.status_code, 200)

        # check if the response shows lots in distance order
        add_distance(response, self.user_location)

        # sorting lots with distance
        sorted_lots = sorted(response.data, key=lambda x: x['distance'])
        self.assertEqual(response.data, sorted_lots)

        for res, lot in zip(response.data, sorted_lots):
            self.assertLessEqual(res['distance'], 1)  # distance between user and lot should be within 1km
            self.assertEqual(res['id'], lot['id'])
            self.assertEqual(res['name'], lot['name'])

    def test_price_odr_list(self):
        response = self.client.get('/api/lots/price_odr', data=self.user_data)
        self.assertEqual(response.status_code, 200)

        # sorting lots with price
        sorted_lots = sorted(response.data, key=lambda x: x['basic_rate'])
        self.assertEqual(response.data, sorted_lots)

        add_distance(response, self.user_location)

        for res, lot in zip(response.data, sorted_lots):
            self.assertLessEqual(res['distance'], 1)  # distance between user and lot should be within 1km
            self.assertEqual(res['id'], lot['id'])
            self.assertEqual(res['name'], lot['name'])


def add_distance(response, user_location):
    """
    response.data -> haversine으로 distance 계산해서 넣어준 리스트를 반환
    """
    for lot in response.data:
        lat = lot['latitude']
        lng = lot['longitude']
        lot_location = (lat, lng)

        distance = haversine(lot_location, user_location)

        lot['distance'] = distance
>>>>>>> 32783878d716984cdc3ce8694fcb3d99e6d24f45
