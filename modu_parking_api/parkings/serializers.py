from rest_framework import serializers
from parkings.models import Parking


class ParkingSerializer(serializers.ModelSerializer):
    """주차 생성, 수정, 삭제, 디테일 시리얼라이저"""

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


class ParkingListSerializer(serializers.ModelSerializer):
    """주차 리스트 시리얼라이저"""
    lot = serializers.StringRelatedField()

    class Meta:
        model = Parking
        fields = (
            'id',
            'lot',
            'parking_time'
        )
