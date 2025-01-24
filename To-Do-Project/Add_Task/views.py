from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import models
from django.http import JsonResponse
from .models import Task
from .forms import ItemForm
import json

# Create your views here.
def get_Task(request,Task_id):
    try:
        task = Task.objects.get(id=Task_id)
        return JsonResponse({
            "TaskName": task.TaskName,
            "Date": task.Date,
            "Priority": task.Priority,         
        })
    except Task.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)
    
def add_Task(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            # Assuming you have a Task model
            task = Task.objects.create(
                TaskName = data.get("TaskName"),
                Date = data.get("Date"),
                Priority = data.get("Priority")
            )
            return JsonResponse({"message": "Task added successfully", "task_id": task.id}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)


#    if request.method == 'POST':
 #       form = ItemForm(request.POST)
  #      if form.is_valid():
   #         form.save()
    #else:
     #   form = ItemForm()