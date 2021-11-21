from django.db import models

from django.contrib.auth.models import AbstractUser


class UserType(models.IntegerChoices):
    GUEST = 1
    EMPLOYEE = 2


class CustomUser(AbstractUser):
    Type = UserType

    type = models.IntegerField(choices=Type.choices, default=Type.GUEST)
