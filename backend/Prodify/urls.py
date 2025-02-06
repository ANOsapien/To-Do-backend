from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path("timetable/", views.api_timetable, name="api_timetable"),
    path("timetable/<int:user>/", views.api_timetable, name="api_timetable_details"),
    path("courses/", views.api_courses, name="api_courses"),
    path("courses/<int:pk>/", views.api_courses, name="api_course_details"),
    path("search/", views.api_search, name="api_search"),
]
