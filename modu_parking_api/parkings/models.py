from django.db import models
from core.models import CoreModel


class Parking(CoreModel):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='parkings')
    lot = models.ForeignKey('lots.Lot', on_delete=models.CASCADE, related_name='parkings')
    start_time = models.DateTimeField(auto_now_add=True)
    parking_time = models.DurationField()  # timedelta 저장
