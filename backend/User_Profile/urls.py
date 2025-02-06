from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', login, name='login'),
    path('get/', views.profile, name='get_user_details'),
    path('edit/', edit_profile, name='edit_own_profile'), 
]