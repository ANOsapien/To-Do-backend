from django.shortcuts import render
from django.http import HttpResponse
from . import models
from django.http import JsonResponse
from .models import UserProfile
import json
from django.views.decorators.csrf import csrf_exempt


def get_UserDetails(request, user_id):
    try:
        user = UserProfile.objects.get(id=user_id)
        return JsonResponse({
            "firstname": user.firstname,
            "lastname": user.lastname,
            "email": user.email,
            "institute": user.institute            
        })
    except models.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)

@csrf_exempt 
def updateRecord(request, user_id):
    print("Request Method:", request.method)  # Debugging
    print("Request Body:", request.body)  # Debugging
    if request.method == 'PUT':
        try:
            user = UserProfile.objects.get(id=user_id)
            data = json.loads(request.body)

            first = data.get('firstname', user.firstname)
            last = data.get('lastname', user.lastname)
            email = data.get('email', user.email)
            institute = data.get('institute', user.institute)

            user.firstname = first
            user.lastname = last
            user.email = email
            user.institute = institute
            user.save()

            return JsonResponse({"message": "User updated successfully"}, status=200)
    

            
        except UserProfile.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)
