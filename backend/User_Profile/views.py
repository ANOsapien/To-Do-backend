from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from .models import UserProfile
from .serializers import UserSerializer, UserProfileSerializer

@api_view(['POST'])
def signup(request):
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')
    first_name = request.data.get('first_name')
    last_name = request.data.get('last_name')
    institute = request.data.get('institute')  # Get institute input
    
    # Validate inputs
    if not all([username, password, email, first_name, last_name, institute]):
        return Response({"error": "All fields are required."}, status=status.HTTP_400_BAD_REQUEST)
    
    # Check if the username already exists
    if User.objects.filter(username=username).exists():
        return Response({"error": "Username already exists."}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = User.objects.create_user(
            username=username, 
            password=password, 
            email=email, 
            first_name=first_name, 
            last_name=last_name
        )
        
        # Create a profile for the user automatically
        UserProfile.objects.create(user=user, institute=institute)

        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
    
    except ValidationError as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception:
        return Response({"error": "An error occurred during signup. Please try again."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def login(request):
    username = request.data.get("username", "").strip()
    password = request.data.get("password", "").strip()

    if not username or not password:
        return JsonResponse({"error": "Username and password are required."}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(request, username=username, password=password)

    if user is not None:
        auth_login(request, user)  # Use Django's built-in login function
        request.session.set_expiry(0)  # Session expires when browser closes
        return JsonResponse({"message": "Login successful"}, status=status.HTTP_200_OK)

    return JsonResponse({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

@login_required   
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile(request):
    user = request.user  # Get logged-in user
    profile = user.userprofile  # Assuming OneToOne relationship with UserProfile

    return JsonResponse({
        "username": user.username,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "institute": profile.institute if profile else None
    }, status=status.HTTP_200_OK)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def edit_profile(request):
    user = request.user  # Get the logged-in user

    profile, created = UserProfile.objects.get_or_create(user=user)
    serializer = UserProfileSerializer(profile, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


