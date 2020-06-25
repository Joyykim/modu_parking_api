from rest_framework.test import APITestCase
from lots.models import Lot
from haversine import haversine


class LotsTestCase(APITestCase):

    def setUp(self) -> None:
        self.lat = 37.5
        self.lng = 126.5
        self.zoom_lv = 2

        # create lots with different location
        for i in range(50):
            Lot.objects.create(latitude=self.lat, longitude=self.lng, name=f'{i}lot', )
            self.lat += 0.05
            self.lng += 0.01

        self.user_data = {
            'latitude': self.lat,
            'longitude': self.lng,
        }

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
            self.assertLessEqual(distance, 2)  # distance between user and lot should be within 2km

    def test_distance_odr_list(self):

        response = self.client.get('/api/lots/distance_odr', data=self.user_data)
        self.assertEqual(response.status_code, 200)

        # check if the response shows lots in distance order
        user_location = (self.lat, self.lng)
        for lot in response.data:
            lat = lot['latitude']
            lng = lot['longitude']
            lot_location = (lat, lng)

            distance = haversine(lot_location, user_location)

            lot['distance'] = distance

        # sorting lots with distance
        sorted_lots = sorted(response.data, key=lambda x: x['distance'])
        for res, lot in zip(response.data, sorted_lots):
            self.assertEqual(res['id'], lot.id)
            self.assertEqual(res['name'], lot.name)
        # self.assertEqual(response.data, sorted_lots)

    def test_price_odr_list(self):
        response = self.client.get('/api/lots/price_odr', data=self.user_data)
        self.assertEqual(response.status_code, 200)

        # sorting lots with price
        sorted_lots = sorted(response.data, key=lambda x: x['basic_rate'])

        for res, lot in zip(response.data, sorted_lots):
            self.assertEqual(res['id'], lot.id)
            self.assertEqual(res['name'], lot.name)
