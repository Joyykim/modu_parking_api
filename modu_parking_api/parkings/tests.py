from random import *
from model_bakery import baker
from munch import Munch
from rest_framework import status
from rest_framework.test import APITestCase
from lots.models import Lot
from parkings.models import Parking
from users.models import User


class ParkingCreateTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = baker.make(User)
        self.lots = baker.make(Lot, _quantity=3)
        self.client.force_authenticate(user=self.user)

    def test_parking_create(self):
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


class ParkingsListTestCase(APITestCase):

    def setUp(self) -> None:
        lots = baker.make(Lot, _quantity=10)
        users = baker.make(User, _quantity=10)
        for user in users:
            for lot in lots:
                Parking.objects.create(lot=lot, user=user, parking_time=randint(1, 5))
        self.user = users[0]
        self.client.force_authenticate(user=self.user)
        self.parking = Parking.objects.first()

    def test_list(self):
        response = self.client.get(f'/api/parkings')
        self.assertEqual(response.status_code, 200)

        for parking in list(response.data):
            # 응답으로 온 parking들이 유저의 parking이 맞는지 테스트
            self.assertEqual(Parking.objects.get(pk=parking['id']).user, self.user)

    def test_update(self):
        prev_parking_time = self.parking.parking_time
        data = {'additional_time': randint(1, 10) / 2}
        response = self.client.put(f'/api/parkings/{self.parking.id}', data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 수정 전 parking_time에 additional_time만큼 플러스가 되었는지 테스트
        self.assertEqual(data['additional_time'] + prev_parking_time, response.data['parking_time'])
