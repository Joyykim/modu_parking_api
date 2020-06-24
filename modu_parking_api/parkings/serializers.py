from datetime import timedelta

from rest_framework import serializers
from django.contrib.auth.models import User
# from lots.serializers import lotSerializer
# from users.serializers import UserSerializer
import lots
from parkings.models import Parking


class ParkingSerializer(serializers.ModelSerializer):
    # lot = lotSerializer(many=True, read_only=True, source='lot_sets')
    # user = UserSerializer(many=True, read_only=True, source='user_sets')

    class Meta:
        models = Parking
        fields = ('id', 'user', 'lot', 'total_fee', 'start_time', 'parking_time', 'current_stat',)


class ParkingTotalFeeSerializer(serializers.ModelSerializer):
    total_fee = serializers.SerializerMethodField()
    t = timedelta(minutes=60)

    class Meta:
        models = Parking
        fields = ['user', 'lot', 'start_time', 'parking_time', 'is_parked', 'end_time', 'extension_time',
                  'extension_rate', 'total_fee']

    # def get_total_fee(self, obj, parking_time, t):
    #     return (lots.basic_rate + (lots.additionalRate * (parking_time - t)))
