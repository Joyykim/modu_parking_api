from rest_framework import serializers
from lots.serializers import LotsSerializer
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
        # list vs tuple
        fields = (
            'id',
            'lot',
            'start_time',
            'parking_time',
            'user',
        )
        read_only_fields = ('id', 'start_time', 'user')

    def _validate(self, attrs):
        lot = Lot.objects.get(id=attrs['lot'])
        parking_time = attrs['parking_time']
        additional_rate = ((parking_time - 1) * 2) * lot.additional_rate  # 추가비용
        total_fee = (lot.basic_rate + additional_rate)  # 총비용

        # 포인트 부족시 거부
        if self.context['request'].user.points < total_fee:
            raise serializers.ValidationError({'refuse': '보유한 포인트가 부족합니다'})

        return attrs


class ParkingUpdateSerializer(serializers.ModelSerializer):
    """주차 수정 시리얼라이저"""
    # singular vs plural
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
