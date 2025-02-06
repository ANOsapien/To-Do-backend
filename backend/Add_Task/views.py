from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Task
from .serializers import TaskSerializer

# ----------------- API Views ------------------

@api_view(['GET'])
@permission_classes([IsAuthenticated])  # User must be logged in
def get_Task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    serializer = TaskSerializer(task)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_task(request):
    serializer = TaskSerializer(data=request.data)
    if serializer.is_valid():
        task = serializer.save(user=request.user)  # Assign task to logged-in user
        return Response(TaskSerializer(task).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.delete()
    return Response({"message": "Task deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def mark_completed(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.completed = True
    task.save()
    return Response(TaskSerializer(task).data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def notification_api(request):
    now = timezone.now().date()
    user_tasks = Task.objects.filter(user=request.user, completed=False)

    overdue_tasks = user_tasks.filter(due_date__lt=now)
    due_today_tasks = user_tasks.filter(due_date=now)
    future_tasks = user_tasks.filter(due_date__gt=now)  # Tasks with a due date in the future

    return Response({
        "overdue_tasks": TaskSerializer(overdue_tasks, many=True).data,
        "due_today_tasks": TaskSerializer(due_today_tasks, many=True).data,
        "future_tasks": TaskSerializer(future_tasks, many=True).data,  # Include future tasks
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def task_list_api(request):
    tasks = Task.objects.filter(user=request.user).order_by('priority', 'due_date')
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)
