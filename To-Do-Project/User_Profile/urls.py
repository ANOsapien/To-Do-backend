from django.urls import path
from . import views

urlpatterns = [
    path('get/<int:user_id>/', views.get_UserDetails, name='get_user_details'),
    path('edit/<int:user_id>/', views.updateRecord, name='edit_user_details')
]