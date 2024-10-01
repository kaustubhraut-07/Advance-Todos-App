from django.contrib import admin
from django.urls import path

from .views import register, login, update_user,google_login

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login , name='login'),
    path('updateuserinfo/', update_user , name='update_user'),
    path('google-login/', google_login, name='google-login'),
]
