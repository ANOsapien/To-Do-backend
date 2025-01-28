from django.contrib import admin
from django.urls import path, include
from . import views
from .views import authView, mainpage

urlpatterns = [
    path("", mainpage, name="mainpage"),
    path("admin/", admin.site.urls),
    path("signup/", authView, name="signup"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("todos/", views.todo_list, name="todo_list"),
    path("todos/<int:pk>/", views.todo_details, name="todo_details"),
    path("timetable/", views.api_timetable, name="api_timetable"),
    path("timetable/<int:user>/", views.api_timetable, name="api_timetable_details"),
    path("courses/", views.api_courses, name="api_courses"),
    path("courses/<int:pk>/", views.api_courses, name="api_course_details"),
    path("search/", views.api_search, name="api_search"),
]