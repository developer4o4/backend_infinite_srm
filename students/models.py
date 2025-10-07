import uuid
from django.db import models
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password
from groups.models import Groups
class Students(models.Model):
    class Status(models.TextChoices):
        APPROVED = "approved", "Tasdiqlangan"
        NOT_CONFIRMED = "not_confirmed", "Tasdiqlanmadi"
        GROUP = "group", "Grupada"
    
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=128)  # Hash uchun
    phone_number = models.CharField(max_length=50)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    status = models.CharField(
        max_length=30,
        choices=Status.choices,
        default=Status.NOT_CONFIRMED,
    )
    about_student = models.TextField(blank=True,default="")
    role = models.CharField(max_length=50, default="student")
    admistrator = models.CharField(max_length=100)
    created_ad = models.DateTimeField(default=timezone.now)
    groups = models.ManyToManyField(Groups, related_name="students", blank=True)
    def set_password(self, raw_password):
        """Parolni hash qilish"""
        self.password = make_password(raw_password)
    
    def check_password(self, raw_password):
        """Parolni tekshirish"""
        return check_password(raw_password, self.password)
    
    def save(self, *args, **kwargs):
        """Agar parol hash qilinmagan bo'lsa, avtomatik hash qilish"""
        if not self.password.startswith('pbkdf2_sha256$'):
            self.set_password(self.password)
        super().save(*args, **kwargs)