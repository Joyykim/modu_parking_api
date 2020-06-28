from rest_framework import serializers
from lots.models import Lot


class LotsSerializer(serializers.ModelSerializer):
    """주차장 생성, 수정, 디테일 용 시리얼라이저"""
    class Meta:
        model = Lot
        fields = ['name', 'address', 'latitude', 'longitude', 'basic_rate', 'additional_rate',
                  'time_weekdays', 'time_weekends', 'section_count', ]


class MapSerializer(serializers.ModelSerializer):
    """리스트 : 지도에서 줌레벨, 좌표로 필터링 하는 시리얼라이저"""
    class Meta:
        model = Lot
        fields = ['id', 'latitude', 'longitude', 'basic_rate', ]
