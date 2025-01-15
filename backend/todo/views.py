from django.shortcuts import render , get_object_or_404, redirect
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .serializers import TodoSerializer
from .models import Todo
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

# Create your views here.
def authView(request):
     if request.method == "POST":
         form= UserCreationForm(request.POST or None)
         if form.is_valid():
              form.save()
              return redirect("todo:regsuccessmsg")
     else:
         form= UserCreationForm()
     return render(request, "signup.html", {"form": form})

@login_required
def mainpage(request):
     return render(request, "mainpage.html")

@api_view(["GET", "POST"])
def todo_list(request):
    if request.method =="GET":
        todos = Todo.objects.all()
        serializer= TodoSerializer(todos, many=True)
        return Response(serializer.data)
    
    elif request.method == "POST":
        serializer= TodoSerializer(data = request.data) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status= status.HTTP_201_CREATED) 
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)

@api_view(["GET","PATCH","PUT","DELETE"])
def todo_details(request, pk):
    todo= get_object_or_404(Todo, id=pk)
    if request.method == "GET":
            serializer=TodoSerializer(todo)
            return Response(serializer.data)
    
    elif request.method == "PUT":
        serializer= TodoSerializer(todo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
    
    elif request.method == "DELETE":
         todo.delete()
         return Response(status=status.HTTP_204_NO_CONTENT)
         
    