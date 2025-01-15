from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Todo(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField(null=True,blank=True)
    completed = models.BooleanField(default=False)

    def _str_(self):
        return self.title