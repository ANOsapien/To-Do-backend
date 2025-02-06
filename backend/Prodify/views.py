from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from .serializers import CourseSerializer, TimeTableSerializer
from .models import  Course, Timetable
from rest_framework.decorators import api_view

@api_view(["GET", "POST", "PUT", "DELETE"])
def api_timetable(request, user=None):
    if request.method =="GET":
        if user:
            timetable = Timetable.objects.filter(user=user)
            serializer= TimeTableSerializer(timetable, many=True)
            return Response(serializer.data)
        
        else:
            timetables = Timetable.objects.all()
            serializer= TimeTableSerializer(timetables, many=True)
            return Response(serializer.data)
    
    elif request.method == "POST":
        serializer= TimeTableSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
    
    elif request.method == "PUT":
        course = get_object_or_404(Course, id=user)
        serializer= TimeTableSerializer(course, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
    
    elif request.method == "DELETE":
        course.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    else:
        return Response(status= status.HTTP_400_BAD_REQUEST)

@api_view(["GET", "POST", "PUT", "DELETE"])
def api_courses(request, pk=None):
    if request.method == "GET":
        if pk:
            course = get_object_or_404(Course, id=pk)
            serializer = CourseSerializer(course)
            return Response(serializer.data)
        
        elif request.GET.get("slot"):
            slot = request.GET.get("slot")
            courses = Course.objects.filter(slot=slot)
            serializer = CourseSerializer(courses, many=True)
            return Response(serializer.data)
        
        else:
            courses = Course.objects.all()
            serializer = CourseSerializer(courses, many=True)
            return Response(serializer.data)

    elif request.method == "POST":
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "PUT":
        course = get_object_or_404(Course, id=pk)
        serializer = CourseSerializer(course, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        course = get_object_or_404(Course, id=pk)
        course.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
@api_view(["GET"])
def api_search(request):
    if request.method =="GET":
        course_name = request.GET.get("course_name")
        course_code = request.GET.get("course_code")
        course = Course.objects.filter(course_name=course_name, course_code=course_code)
        if not course.exists():
            return Response({"error": "No courses found matching the criteria."}, status=status.HTTP_404_NOT_FOUND)
        serializer= CourseSerializer(course, many=True)
        return Response(serializer.data)
    
    else:
        return Response(status= status.HTTP_400_BAD_REQUEST)