from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from . import views
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", mainpage, name="mainpage"),
    path('profile/', views.profile_view, name='profile'),
    path('edit-profile/', views.edit_profile_view, name='edit_profile'),
    path("signup/", authView, name="authView"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("todos/",views.task_list),
    path("todos/<int:pk>",views.todo_details),
    path('delete/<int:task_id>/', delete_task, name='delete_task'),
    path('complete/<int:task_id>/', mark_completed, name='mark_completed'),
    path('notifications/', notification_page, name='notifications'),
    ] 
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)