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


class OrderSerializer(serializers.ModelSerializer):
    """리스트 : 가격순, 거리순 정렬 시리얼라이저"""

    class Meta:
        model = Lot
        fields = ['id', 'name', 'basic_rate', 'latitude', 'longitude']  # 'distance'


"""
lots app
POST /lots/
: 주차장 등록
PUT /lots/id
: 주차장 정보수정
GET /lots/id
: 주차장 세부정보

GET /lots/map(action) 
: 주차장 맵뷰역(예: 서울시)

GET /lots/distance_odr(action) 
: 주차장 목록 거리순 정렬
GET /lots/price_odr(action) 
: 주차장 목록 가격순 정렬
DELETE /lots/id 
: 주차장 삭제
"""

