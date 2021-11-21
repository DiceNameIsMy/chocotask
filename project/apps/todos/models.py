from django.db import models

from django.contrib.auth import get_user_model


UserModel = get_user_model()


class PriorityType(models.IntegerChoices):
    LOW = 1
    MEDIUM = 2
    HIGH = 3


class Todo(models.Model):
    Priority = PriorityType

    author = models.ForeignKey(to=UserModel, on_delete=models.SET_NULL, null=True, related_name='todos')

    title = models.CharField(max_length=100)
    description = models.TextField()
    deadline = models.DateTimeField(null=True, blank=True)

    priority = models.IntegerField(choices=Priority.choices, default=Priority.MEDIUM)
    completed = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # If was not notified yet and has deadline in 
    # an hour, send notification
    notified = models.BooleanField(default=False)
