from rest_framework import serializers
from .models import Todo, Course, Timetable

class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ('id', 'title', 'description', 'completed')

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('id', 'course_name', 'course_code', 'course_instructor', 'course_description', 'review', 'ratings', 'start_time', 'end_time', 'slot', 'day')

class TimeTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Timetable
        fields = ('id', 'user', 'course', 'start_time', 'end_time', 'day', 'slot')