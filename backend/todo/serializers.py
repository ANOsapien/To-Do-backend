from rest_framework import serializers
from .models import Todo, Course

class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ('id', 'title', 'description', 'completed')

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('id', 'course_name', 'course_code', 'curse_instructor', 'course_description', 'review', 'ratings', 'start_time', 'end_time', 'slot')