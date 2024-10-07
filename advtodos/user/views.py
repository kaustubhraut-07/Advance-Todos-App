from django.shortcuts import render
from .serializers import CustomUserSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate
from google.oauth2 import id_token
from google.auth.transport import requests
from django.conf import settings
from .models import CustomUser
from rest_framework import status, request

# Create your views here.
# @api_view(['POST'])
# def register(request):
#     if request.method == 'POST':
#         serializer = CustomUserSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


@api_view(['POST'])
def register(request):
    if request.method == 'POST':
       
        serializer = CustomUserSerializer(data=request.data)
        
        if serializer.is_valid():
           
            user = CustomUser(**serializer.validated_data)
            
           
            user.set_password(serializer.validated_data['password'])
            
           
            user.save()
            
           
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
    if request.method == 'POST':
        email = str(request.data.get('email'))
        password = str(request.data.get('password'))
        print(f"Received username: {email}, password: {password}")

        if not email or not password:
            return Response({"error": "Username and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(email= email , password=password)
        print(f"Authenticated user: {user}")

        if user is not None:
            serializer = CustomUserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['PUT'])
def update_user(request):
    email = request.data.get('email')
    if not email:
        return Response({"error": "Username is required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = CustomUser.objects.get(email=email)
    except CustomUser.DoesNotExist:
        return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

    serializer = CustomUserSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_user(request):
    email = request.data.get('email')
    if not email:
        return Response({"error": "Username is required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = CustomUser.objects.get(email=email)
    except CustomUser.DoesNotExist:
        return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

    user.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)




# @api_view(['POST'])
# def google_login(request):
#     token = request.data.get('token')
#     if not token:
#         return Response({"error": "Token is required"}, status=status.HTTP_400_BAD_REQUEST)

#     try:
#         # Verify the token using Google's OAuth2 API
#         idinfo = id_token.verify_oauth2_token(token, requests.Request(), settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY)

#         # Get additional data from the token
#         email = idinfo.get('email')
#         name = idinfo.get('name')
#         oauth_id = idinfo.get('sub')  # Google's unique ID for the user
#         avatar = idinfo.get('picture')

      
#         user, created = CustomUser.objects.get_or_create(email=email, defaults={
#             'email': email,
#             'name': name,
#             'oauth_id': oauth_id,
#             'avatar': avatar,
#             'provider': 'google'
#         })

#         if created:
#             user.set_unusable_password() 
#             user.save()

      
#         serializer = CustomUserSerializer(user)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     except ValueError as e:
#         print(f"Token verification failed: {e}")
#         return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

#     except Exception as e:
#         print(f"An error occurred: {e}")
#         return Response({"error": "An error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def google_login(request):
    token = request.data.get('token')
    if not token:
        return Response({"error": "Token is required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Verify the token using Google's OAuth2 API
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY)

        # Get additional data from the token
        email = idinfo.get('email')
        name = idinfo.get('name')
        oauth_id = idinfo.get('sub')  # Google's unique ID for the user
        avatar = idinfo.get('picture')

        user, created = CustomUser.objects.get_or_create(email=email, defaults={
            'name': name,
            'oauth_id': oauth_id,
            'avatar': avatar,
            'provider': 'google'
        })

        if created:
            user.set_unusable_password()
            user.save()

        serializer = CustomUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except ValueError as e:
        print(f"Token verification failed: {e}")
        return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

    except Exception as e:
        print(f"An error occurred: {e}")
        return Response({"error": "An error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)