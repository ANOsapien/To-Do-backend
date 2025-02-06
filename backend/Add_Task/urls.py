from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('get/<int:task_id>/', get_Task, name='get_task'),
    path('add/', views.add_task),
    path('delete/<int:task_id>/', delete_task, name='delete_task_api'),
    path('complete/<int:task_id>/', mark_completed, name='mark_completed_api'),
    path('notifications/', notification_api, name='notification_api'),
    path('task-list/', task_list_api, name='task-list-api'),
]