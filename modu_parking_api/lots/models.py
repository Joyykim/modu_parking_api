from django.db import models


class Lot(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)
    basic_rate = models.IntegerField(default=0)
    additional_rate = models.IntegerField(default=0)
    time_weekdays = models.CharField(max_length=30, null=True, )
    time_weekends = models.CharField(max_length=30, null=True, )
    section_count = models.IntegerField(default=0)
