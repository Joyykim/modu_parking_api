from rest_framework import serializers

from lots.models import Lot


class LotsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lot
        fields = ('name', 'address', 'phone_num', 'latitude', 'longitude', 'basic_rate', 'additional_rate', 'partnership',
                  'time_weekdays', 'time_weekends', 'section_count',
                                                                     # 'location',
                  )


class MapSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lot
        fields = ('name', 'address', 'phone_num', 'latitude', 'longitude', 'basic_rate', 'additional_rate', 'partnership',
                  'time_weekdays', 'time_weekends', 'section_count', 'filter', 'location', )
        read_only_fields = []
        extra_kwargs = {
            'filter': {'write_only': True}
        }


