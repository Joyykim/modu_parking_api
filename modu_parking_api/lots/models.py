from django.db import models


class Lot(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    # lat/lon default 값 필요 한지 확인
    latitude = models.FloatField()
    longitude = models.FloatField()
    # default 값 필요 한지 확인
    # int -> positivefield
    basic_rate = models.PositiveIntegerField()
    # default 값 필요 한지 확인
    # int -> positivefield
    additional_rate = models.PositiveIntegerField()
    # null=True 필요 한지 확인
    time_weekdays = models.CharField(max_length=30)
    time_weekends = models.CharField(max_length=30)
    # int -> positiveint
    section_count = models.PositiveIntegerField(default=0)
