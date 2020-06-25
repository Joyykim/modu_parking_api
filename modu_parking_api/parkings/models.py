from django.db import models
from lots.models import Lot
from users.models import User


class Parking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='parkings', null=True,)
    lot = models.ForeignKey(Lot, on_delete=models.CASCADE, null=True,)
    start_time = models.DateTimeField(auto_now_add=True, null=True,)
    parking_time = models.DateTimeField(null=True,)
    end_time = models.DateTimeField()
    extension_time = models.DateTimeField()
    extension_rate = models.IntegerField()
    total_fee = models.IntegerField()
