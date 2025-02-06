from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile

class UserSerializer(serializers.ModelSerializer):
    institute = serializers.CharField(source='UserProfile.institute', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'institute']

class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', required=False)
    email = serializers.EmailField(source='user.email', required=False)
    first_name = serializers.CharField(source='user.first_name', required=False)
    last_name = serializers.CharField(source='user.last_name', required=False)
    institute = serializers.CharField(required=False)

    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'first_name', 'last_name', 'institute']

    def validate_username(self, value):
        """Ensure the username is unique"""
        if User.objects.filter(username=value).exclude(id=self.instance.user.id).exists():
            raise serializers.ValidationError("This username is already taken.")
        return value

    def validate_email(self, value):
        """Ensure the email is unique"""
        if User.objects.filter(email=value).exclude(id=self.instance.user.id).exists():
            raise serializers.ValidationError("This email is already taken.")
        return value

    def update(self, instance, validated_data):
        # Extract user data separately
        user_data = validated_data.pop('user', {})

        # Update User model
        user = instance.user
        user.username = user_data.get('username', user.username)
        user.email = user_data.get('email', user.email)
        user.first_name = user_data.get('first_name', user.first_name)
        user.last_name = user_data.get('last_name', user.last_name)
        user.save()  # Save changes to User model

        # Update UserProfile fields
        instance.institute = validated_data.get('institute', instance.institute)
        instance.save()  # Save changes to UserProfile model

        return instance
