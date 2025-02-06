from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'due_date', 'priority', 'completed']  # Exclude 'user'

    def create(self, validated_data):
        request = self.context.get('request')  # Get request context
        if request and request.user.is_authenticated:
            validated_data['user'] = request.user  # Assign logged-in user
        return super().create(validated_data)