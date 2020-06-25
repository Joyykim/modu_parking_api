from django.db import models


class Lot(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    phone_num = models.CharField(max_length=100)
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)
    basic_rate = models.IntegerField(default=0)
    additional_rate = models.IntegerField(default=0)
    partnership = models.BooleanField(default=False)
    time_weekdays = models.CharField(max_length=30, null=True, )
    time_weekends = models.CharField(max_length=30, null=True, )
    section_count = models.IntegerField(default=0)

    # def __str__(self):
    #     return f'{self.name}'

    # distance = db_models.PointField(null=False, blank=False, srid=4326, verbose_name='distance')

    @staticmethod
    def create_model():
        for i in range(3):
            Lot.objects.create(
                name=f'성수 주차장 {i}번지',
                address=f'성수동 {i}번지',
                latitude=127.77,
                longitude=352.123,
                basic_rate=10000 + (i * 1000),
                additional_rate=6000 + (i * 1000),
                partnership=False,
                section_count=i + 1
            )
