# tracker/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser


class TimeRecord(models.Model):
    project = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    notes = models.TextField()

    def __str__(self):
        return f"{self.project} - {self.start_datetime}"


class User(AbstractUser):
    invite_code = models.CharField(max_length=20, blank=True, null=True)


class InviteCode(models.Model):
    code = models.CharField(max_length=20, unique=True)
    uses_left = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.code
