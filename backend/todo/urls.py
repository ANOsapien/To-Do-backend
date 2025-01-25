from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from . import views
from .views import authView, mainpage
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", mainpage, name="mainpage"),
    path('profile/', views.profile_view, name='profile'),
    path('edit-profile/', views.edit_profile_view, name='edit_profile'),
    path("signup/", authView, name="authView"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("todos/",views.todo_list),
    path("todos/<int:pk>",views.todo_details),
    ] 
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)