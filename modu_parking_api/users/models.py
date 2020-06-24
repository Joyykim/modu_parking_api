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
    username = models.CharField(max_length=30, blank=True, null=True)
    phoneNum = models.IntegerField(default=None, blank=True, null=True)
    plateNum = models.CharField(default=None, blank=True, null=True, max_length=20)
    cardNum = models.IntegerField(default=None, blank=True, null=True)
    points = models.IntegerField(default=0)
    bookmark = models.ManyToManyField(Lot, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    objects = UserManager()  # Replace the default model manager with custom UserManager
    USERNAME_FIELD = 'email'  # Set the USERNAME_FIELD (which defines the unique identifier for the User model) to email
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    @staticmethod
    def create_model():
        for i in range(3):
            User.objects.create(
                email=f'user{i}@co.com',
                username=f'사용자{i}',
                password=1111,
            )
