from django.db import models


class Lot(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    phone_num = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    basicRate = models.IntegerField()
    additionalRate = models.IntegerField()
    partnership = models.BooleanField(default=False)
    time_weekdays = models.CharField(max_length=30)
    time_weekends = models.CharField(max_length=30)
