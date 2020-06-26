from datetime import timedelta

from rest_framework import serializers
from django.contrib.auth.models import User
from lots.serializers import LotsSerializer
from users.serializers import UserSerializer
import lots
from parkings.models import Parking


class ParkingSerializer(serializers.ModelSerializer):
    """주차 생성, 삭제, 디테일 시리얼라이저

    생성:
    request = lot, parking_time
    response = id, lot(foreign), start_time, parking_time

    디테일 - 사용자의 주차 내역만 조회가능:
    response = id, lot(foreign), start_time, parking_time

    리스트 - 사용자의 주차내역 목록:
    response = id, lot(foreign), parking_time

    삭제:
    response = 204

    수정:
    request = additional_time
    response = id, lot(foreign), start_time, parking_time
    """

    class Meta:
        model = Parking
        fields = (
            'id',
            'lot',
            'start_time',
            'parking_time',
            'user',
        )
        read_only_fields = ('id', 'start_time', 'user')


class ParkingUpdateSerializer(serializers.ModelSerializer):
    """주차 수정 시리얼라이저"""
    lot = LotsSerializer()

    class Meta:
        model = Parking
        fields = (
            'id',
            'lot',
            'start_time',
            'parking_time',
        )
        read_only_fields = ('id', 'lot', 'start_time', 'parking_time',)


class ParkingListSerializer(serializers.ModelSerializer):
    """주차 리스트 시리얼라이저"""
    lot = LotsSerializer()

    class Meta:
        model = Parking
        fields = (
            'id',
            'lot',
            'parking_time'
        )
