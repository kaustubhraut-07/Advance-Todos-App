from django.contrib import admin
from django.urls import path

from .views import register, login, update_user

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login , name='login'),
    path('updateuserinfo/', update_user , name='update_user'),
]
