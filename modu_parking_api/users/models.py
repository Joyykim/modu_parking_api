from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractUser
from lots.models import Lot


class UserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of username.
    A manager is an interface through which database query operations are provided to Django models.
    """

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email, username and password.
        """
        if not email:
            raise ValueError('The email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """
    Use an email address as the primary user identifier instead of a username for authentication
    """
    email = models.EmailField(max_length=100, unique=True, verbose_name='email')
    # null vs default=''
    username = models.CharField(max_length=30, blank=True, default='')
    # camel -> snake
    # 부가 적인 정보는 profile OneToOne 모델로 추출
    # https://docs.djangoproject.com/en/3.0/topics/auth/customizing/#extending-the-existing-user-models
    phoneNum = models.CharField(max_length=20, default=None, blank=True, null=True)
    plateNum = models.CharField(max_length=20, default=None, blank=True, null=True)
    cardNum = models.CharField(max_length=20, default=None, blank=True, null=True)
    points = models.IntegerField(default=0)
    # 자주사용 하는 모델 필드는 Abstract Model 추출
    # https://docs.djangoproject.com/en/3.0/topics/db/models/#abstract-base-classes
    created = models.DateTimeField(auto_now_add=True)

    objects = UserManager()  # Replace the default model manager with custom UserManager
    USERNAME_FIELD = 'email'  # Set the USERNAME_FIELD (which defines the unique identifier for the User model) to email
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class BookMark(models.Model):
    """주차장 즐겨찾기"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lot = models.ForeignKey(Lot, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
