from django.db import models

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager


class UserType(models.IntegerChoices):
    GUEST = 1
    EMPLOYEE = 2


class CustomUserManager(UserManager):
    def create_superuser(self, *args, **kwargs):
        kwargs['type'] = UserType.EMPLOYEE
        return super().create_superuser(*args, **kwargs)


class CustomUser(AbstractUser):
    Type = UserType

    type = models.IntegerField(choices=Type.choices, default=Type.GUEST)

    objects = CustomUserManager()
