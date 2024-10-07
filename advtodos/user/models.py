
from django.contrib.auth.models import AbstractUser ,BaseUserManager
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

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)
class CustomUser(AbstractUser, models.Model):
    name= models.CharField(max_length=255, null=False, blank=False)
    email = models.EmailField(unique=True,null=False, blank=False)
    oauth_id = models.CharField(max_length=255,default="default_oauth_id", blank=True)
    avatar = models.CharField(max_length=255, null=True, blank=True)
    provider=models.CharField(max_length=255 ,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']


    def __str__(self):
        return self.email
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.username = self.email
        super().save(*args, **kwargs)