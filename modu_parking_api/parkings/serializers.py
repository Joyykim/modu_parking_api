from datetime import timedelta

from rest_framework import serializers
from django.contrib.auth.models import User
from lots.serializers import LotsSerializer
from users.serializers import UserSerializer
import lots
from parkings.models import Parking


class ParkingSerializer(serializers.ModelSerializer):
    lot = LotsSerializer(many=True, read_only=True, source='lot_sets')
    user = UserSerializer(many=True, read_only=True, source='user_sets')

    # total_fee 계산 재료
    original_rate = LotsSerializer  # lot에서 가져옴

    class Meta:
        models = Parking
        fields = ('id', 'user', 'lot', 'total_fee', 'start_time', 'end_time', 'parking_time',
                  'current_stat', 'extension_rate', 'extension_time', 'original_rate')


class ParkingListSerializer(serializers.ModelSerializer):
    lot = serializers.StringRelatedField()

    class Meta:
        models = Parking
        fields = ('id', 'total_fee', 'parking_time', 'lot')
