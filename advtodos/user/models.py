
from django.contrib.auth.models import AbstractUser
from django.db import models

# class CustomUser(AbstractUser, models.Model):
#     username = models.CharField(max_length=255, unique=True , null=False, blank=False)
#     name= models.CharField(max_length=255, null=False, blank=False)
#     email = models.EmailField(unique=True,null=False, blank=False)
#     password = models.CharField(max_length=255,null=False,blank=False)
#     avatar = models.ImageField(upload_to='uploads/avatars/', null=True, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.username
class CustomUser(AbstractUser, models.Model):
    name= models.CharField(max_length=255, null=False, blank=False)
    email = models.EmailField(unique=True,null=False, blank=False)
    oauth_id = models.CharField(max_length=255,default="default_oauth_id", blank=True)
    avatar = models.CharField(max_length=255, null=True, blank=True)
    provider=models.CharField(max_length=255 ,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username