from django.test import TestCase

import copy
from random import *
from haversine import haversine
from model_bakery import baker
from rest_framework import status
from rest_framework.test import APITestCase

from lots.models import Lot
from parkings.models import Parking
from users.models import User


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
