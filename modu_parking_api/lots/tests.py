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

from model_bakery import baker
from munch import Munch
from rest_framework import status
from rest_framework.test import APITestCase

from lots.models import Lot
from haversine import haversine


class UrlTestCase(APITestCase):
    """
    URL 히스토리(list - 자신의 히스토리만)
    """

    def setUp(self) -> None:
        self.lat = 37.5
        self.lng = 126.5
        self.zoom_lv = 2

        for i in range(50):
            Lot.objects.create(latitude=self.lat, longitude=self.lng, name=f'{i}lot', )
            self.lat += 0.05
            self.lng += 0.01
        self.position = {
            'latitude': "",
            'longitude': ''
        }

    def test_map(self):
        """
        GET /lots/map(action)
        리스트 : 지도에서 줌레벨, 좌표로 필터링
        주차장 맵뷰역(예: 서울시)
        """
        data = {
            # 사용자 위치정보,
            'latitude': self.lat,
            'longitude': self.lng,
            'zoom_lv': self.zoom_lv
        }
        response = self.client.get('/api/lots', data=data)


        self.assertEqual(response.status_code, 200)
        # res = Munch(response.data)
        user_position = (self.lat, self.lng)  # (lat, lon)
        for lot in response.data:
            lat = lot['latitude']
            lng = lot['longitude']
            res = (lat, lng)
            distance = haversine(res, user_position)

            # 반경 테스트(2키로 반경 내에 있는 주차장인지)
            self.assertLessEqual(distance, 2)

            # name 테스트
            self.assertTrue()

    def test_distance_odr(self):
        """
        GET /lots/distance_odr(action)
        : 주차장 목록 거리순 정렬
        """
        data = {

        }

    def test_price_odr(self):
        """
        GET /lots/price_odr(action)
        : 주차장 목록 가격순 정렬
        """

