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
        #     self.assertEqual(res['id'], lot['id'])
        #     self.assertEqual(res['name'], lot['name'])

    def test_price_odr_list(self):
        response = self.client.get('/api/lots/price_odr', data=self.user_data)
        self.assertEqual(response.status_code, 200)

        # sorting lots with price
        sorted_lots = sorted(response.data, key=lambda x: x['basic_rate'])
        self.assertEqual(response.data, sorted_lots)

        add_distance(response, self.user_location)

        for res, lot in zip(response.data, sorted_lots):
            self.assertLessEqual(res['distance'], 1)  # distance between user and lot should be within 1km
        #     self.assertEqual(res['id'], lot['id'])
        #     self.assertEqual(res['name'], lot['name'])


def add_distance(response, user_location):
    """
    haversine으로 distance 계산해서 넣어준 리스트를 반환
    """
    for lot in response.data:
        lat = lot['latitude']
        lng = lot['longitude']
        lot_location = (lat, lng)

        distance = haversine(lot_location, user_location)

        lot['distance'] = distance
