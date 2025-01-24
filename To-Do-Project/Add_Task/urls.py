from django.urls import path
from . import views

urlpatterns = [
    path('get/<int:Task_id>/', views.get_Task),
    path('add/', views.add_Task)
]