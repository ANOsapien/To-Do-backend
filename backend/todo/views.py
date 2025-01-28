from django.shortcuts import render , get_object_or_404, redirect
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .serializers import TaskSerializer
from django.contrib.auth.decorators import login_required
from .models import Profile
from .forms import ProfileForm
from django.contrib.auth import login
from .forms import CustomUserCreationForm
from .forms import TaskForm
from .models import Task
from django.utils import timezone


# Create your views here.
def authView(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) 
            return redirect('mainpage')  
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})

@login_required
def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    return render(request, 'profile.html', {
        'profile': profile,
        'has_profile_picture': bool(profile.profile_picture and profile.profile_picture.name),
    })

@login_required
def mainpage(request):
    if request.method == "POST":
        title = request.POST.get('title')
        due_date = request.POST.get('due_date')
        priority = request.POST.get('priority')

        Task.objects.create(
            user=request.user,
            title=title,
            due_date=due_date,
            priority=priority
        )
        return redirect('todo:mainpage')  # Redirect to avoid duplicate form submissions

    # Sorting tasks first by priority (ascending), then by due_date (ascending)
    tasks = Task.objects.filter(user=request.user).order_by('priority', 'due_date')

    return render(request, 'mainpage.html', {'tasks': tasks})

@login_required
def edit_profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'edit_profile.html', {'form': form})

@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user)
    return render(request, 'task_list.html', {'tasks': tasks})

@login_required
def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user  # Assign task to the logged-in user
            task.save()
            return redirect('task_list')
    else:
        form = TaskForm()

    return render(request, 'add_task.html', {'form': form})

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.delete()
    return redirect('todo:mainpage')

@login_required
def mark_completed(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.completed = True
    task.save()
    return redirect('todo:mainpage')

@api_view(["GET","PATCH","PUT","DELETE"])
def todo_details(request, pk):
    todo= get_object_or_404(Task, id=pk)
    if request.method == "GET":
            serializer=TaskSerializer(todo)
            return Response(serializer.data)
    
    elif request.method == "PUT":
        serializer= TaskSerializer(todo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
    
    elif request.method == "DELETE":
         todo.delete()
         return Response(status=status.HTTP_204_NO_CONTENT)
         
def notification_page(request):
    now = timezone.now().date()
    overdue_tasks = Task.objects.filter(due_date__lt=now, completed=False)
    due_today_tasks = Task.objects.filter(due_date=now, completed=False)

    context = {
        "overdue_tasks": overdue_tasks,
        "due_today_tasks": due_today_tasks
    }
    
    return render(request, "notifications.html", context)