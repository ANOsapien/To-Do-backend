from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# Create your models here.
class Task(models.Model):
    PRIORITY_CHOICES = [
        ('1', 'Priority 1'),  # High (Red)
        ('2', 'Priority 2'),  # Medium-High (Orange)
        ('3', 'Priority 3'),  # Medium (Blue)
        ('4', 'Priority 4'),  # Low (Green)
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=255)
    due_date = models.DateField(default=now)
    priority = models.CharField(max_length=1, choices=PRIORITY_CHOICES, default='3')
    completed = models.BooleanField(default=False)