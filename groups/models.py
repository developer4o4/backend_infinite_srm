from django.db import models
from teachers.models import Teachers
from django.utils import timezone


class Groups(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "active", "Faol"
        INACTIVE = "inactive", "Tugagan"

    title = models.CharField(max_length=50)
    teacher = models.ForeignKey(Teachers,on_delete=models.DO_NOTHING)
    group_price = models.IntegerField(default=0)
    status = models.CharField(
        max_length=30,
        choices=Status.choices,
        default=Status.ACTIVE,
    )
    hwo_created = models.CharField(max_length=100,default='admin')
    group_time = models.CharField(default="Dushanba,Chorshanba,Juma 14:00-16:00")
    created_at = models.DateTimeField(default=timezone.now)