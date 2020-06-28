from django.db import models


class Lot(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    basic_rate = models.PositiveIntegerField()
    additional_rate = models.PositiveIntegerField()
    time_weekdays = models.CharField(max_length=30)
    time_weekends = models.CharField(max_length=30)
    section_count = models.PositiveIntegerField()
