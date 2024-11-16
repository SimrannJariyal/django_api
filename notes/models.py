from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)  # Enforce unique email
    username = models.CharField(max_length=150, blank=True, null=True)  # Username not required and not unique

    USERNAME_FIELD = 'email'  # Use email as the identifier for the user
    REQUIRED_FIELDS = ['username']  # Make username required for admin interface, but not unique

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
