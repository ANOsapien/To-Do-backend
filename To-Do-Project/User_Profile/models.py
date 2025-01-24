from django.db import models

# Create your models here.
class UserProfile(models.Model):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    email = models.EmailField(max_length = 255)
    institute = models.CharField(max_length=255)