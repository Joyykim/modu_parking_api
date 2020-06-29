from django.db import models
from lots.models import Lot
from users.models import User


class Parking(models.Model):
    # FK 연결은 Class가 아니라 str으로 사용해서 순환참조 방지: https: // code.djangoproject.com / ticket / 167
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='parkings')
    # user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='parkings')
    lot = models.ForeignKey(Lot, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)
    # DurationField 사용 https://docs.djangoproject.com/en/3.0/ref/models/fields/#durationfield
    # default 사용 확인
    parking_time = models.FloatField(default=0.0)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        is_created = self.id is None

        parking = super().save(force_insert=False, force_update=False, using=None,
             update_fields=None)

        if is_created:
            # self.user...
            pass

        return parking
