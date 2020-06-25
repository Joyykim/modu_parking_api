from datetime import timedelta

from rest_framework import serializers
from django.contrib.auth.models import User
from lots.serializers import LotsSerializer
from users.serializers import UserSerializer
import lots
from parkings.models import Parking


class ParkingSerializer(serializers.ModelSerializer):
    """주차 생성, 수정, 삭제, 디테일 시리얼라이저"""

    class Meta:
        models = Parking
        fields = (
            'id',
            'lot',
            'start_time',
            'parking_time',
        )


class ParkingListSerializer(serializers.ModelSerializer):
    """주차 리스트 시리얼라이저"""
    lot = serializers.StringRelatedField()

    class Meta:
        models = Parking
        fields = (
            'id',
            'lot',
            'parking_time'
        )
