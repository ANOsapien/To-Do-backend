from django.db import models

# Create your models here.
class Task(models.Model):
    TaskName = models.CharField(max_length=255)
    Date = models.DateField()
    Priority = models.IntegerField()
