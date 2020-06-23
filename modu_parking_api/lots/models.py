from django.db import models
from django.contrib.gis.db import models

class Lot(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    phone_num = models.CharField(max_length=100)
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)
    basic_rate = models.IntegerField(default=0)
    additional_rate = models.IntegerField(default=0)
    partnership = models.BooleanField(default=False)
    time_weekdays = models.CharField(max_length=30)
    time_weekends = models.CharField(max_length=30)
    section_count = models.IntegerField(default=0)
    distance = models.PointField(null=False, blank=False, srid=4326, verbose_name='distance')
