from django.db import models
from lots.models import Lot
from users.models import User
from lots.models import basicRate, additionalRate

class Parking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='parkings')
    lot = models.ForeignKey(Lot, on_delete=models.CASCADE)
    basicRate = models.ForeignKey(basicRate, on_delete=models.CASCADE)
    additionalRate = models.ForeignKey(additionalRate, on_delete=models.CASCADE)
    total_fee = models.IntegerField(default=0)
    start_time = models.DateTimeField(auto_now_add=True)
    parking_time = models.DateTimeField()
    current_stat = models.BooleanField()