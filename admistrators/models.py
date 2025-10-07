from django.db import models
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password

class Admin_users(models.Model):
    profile_img = models.FileField(upload_to='media/profile_images',default="profile.png")
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    direction = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=30)
    role = models.CharField(max_length=50,default="adminstrator")
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.username

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