from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from . import views
from .views import authView, mainpage

urlpatterns = [
    path("", mainpage, name="mainpage"),
    path("signup/", authView, name="authView"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("todos/",views.todo_list),
    path("todos/<int:pk>",views.todo_details),
    ] 