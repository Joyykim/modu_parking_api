from django.db import models


class Lot(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    # lat/lon default 값 필요 한지 확인
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)
    # default 값 필요 한지 확인
    # int -> positivefield
    basic_rate = models.IntegerField(default=0)
    # default 값 필요 한지 확인
    # int -> positivefield
    additional_rate = models.IntegerField(default=0)
    # null=True 필요 한지 확인
    time_weekdays = models.CharField(max_length=30, null=True)
    time_weekends = models.CharField(max_length=30, null=True)
    # int -> positiveint
    section_count = models.IntegerField(default=0)
