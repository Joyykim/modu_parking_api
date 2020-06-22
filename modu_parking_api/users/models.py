from django.db import models

from django.contrib.auth.models import AbstractUser

from lots.models import Lot


class User(AbstractUser):
    email = models.EmailField(unique=True)
    phoneNum = models.IntegerField()
    plateNum = models.CharField(max_length=20)
    cardNum = models.IntegerField()
    points = models.IntegerField()
    bookmark = models.ManyToManyField(Lot)


class Payment(models.Model):
    amount = models.IntegerField(default=0)
    time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
