from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, blank=True, null=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username if self.username else self.email

class Subject(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    sub_icon = models.ImageField(upload_to='subject_icons/', null=True, blank=True)

    def __str__(self):
        return self.name

class Unit(models.Model):
    unit_name = models.CharField(max_length=100)
    pdf_file = models.FileField(upload_to='units/')
    subject = models.ForeignKey(Subject, related_name='units', on_delete=models.CASCADE)

    def __str__(self):
        return self.unit_name
from django.conf import settings
from django.db import models
class Task(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_completed = models.BooleanField(default=False)

