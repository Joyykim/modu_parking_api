from model_bakery import baker
from munch import Munch
from rest_framework.test import APITestCase
from lots.models import Lot
from users.models import User


class ParkingCreateTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = baker.make(User)
        self.lots = baker.make(Lot, _quantity=3)
        self.client.force_authenticate(user=self.user)

    def test_link_create(self):
        url = '/api/parkings'
        data = {
            "lot": self.lots[0].id,
            "parking_time": 3,
        }

        response = self.client.post(url, data=data)
        self.assertEqual(201, response.status_code)

        res = Munch(response.data)
        self.assertTrue(res.id)
        self.assertEqual(res.parking_time, data['parking_time'])
        self.assertEqual(res.user, self.user.id)


