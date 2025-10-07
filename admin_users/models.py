from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class Admin_users(AbstractUser):
    phone_number = models.CharField(max_length=80)
    created_at = models.DateTimeField(default=timezone.now)
    role = models.CharField(max_length=50,default="admin")
    def __str__(self):
        return self.username


