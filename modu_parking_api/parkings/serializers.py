from rest_framework import serializers
from django.contrib.auth.models import User
# from lots.serializers import lotSerializer
# from users.serializers import UserSerializer

from parkings.models import Parking


class ParkingSerializer(serializers.ModelSerializer):
    # lot = lotSerializer(many=True, read_only=True, source='lot_sets')
    # user = UserSerializer(many=True, read_only=True, source='user_sets')

    class Meta:
        models = Parking
        fields = ('id', 'user', 'lot', 'total_fee', 'start_time', 'parking_time', 'current_stat',)

