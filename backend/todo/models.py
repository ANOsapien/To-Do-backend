from django.db import models
from django.contrib.auth.models import User
from .constants import SLOT_CHOICES, LAB_CHOICES
from .utils import get_slot_timing

# Create your models here.
class Todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    completed = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ["completed", "-created"]
    
class Course(models.Model):
    course_name = models.CharField(max_length=200)
    course_code = models.CharField(max_length=200)
    course_instructor = models.CharField(max_length=200, null=True, blank=True)
    course_description = models.TextField(null=True, blank=True)
    review = models.TextField(null=True, blank=True)
    ratings = models.FloatField(null=True, blank=True)

    # Time-related fields
    slot = models.CharField(
        max_length=200,
        choices=SLOT_CHOICES + LAB_CHOICES,
        null=True,
        blank=True
    )
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    day = models.CharField(max_length=200, null=True, blank=True)

    def clean(self):
        if self.slot:
            # Auto-fill start_time and end_time based on slot
            slot_info = get_slot_timing(self.slot)
            if slot_info:
                self.start_time = slot_info['start']
                self.end_time = slot_info['end']
                self.day = slot_info['day']

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.course_name
    
    class Meta:
        ordering = ['course_name']

class Timetable(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    slot = models.CharField(max_length=200, choices=SLOT_CHOICES + LAB_CHOICES, null=True, blank=True)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    day = models.CharField(max_length=200, null=True, blank=True)
    
    def clean(self):
        if self.slot:
            slot_info = get_slot_timing(self.slot)
            if slot_info:
                self.start_time = slot_info['start']
                self.end_time = slot_info['end']
                self.day = slot_info['day']

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.course.course_name
    
    class Meta:
        ordering = ['slot']