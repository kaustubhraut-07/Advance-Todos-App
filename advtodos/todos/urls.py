from django.contrib import admin
from django.urls import path
from .views import getallTodosforUser,createTodo,updateTodo,deleteTodo

urlpatterns = [
    path('getalltodosbyuseremail/<str:email>/', getallTodosforUser , name='getallTodosforUser'),
    path('createTododo/<str:email>/' ,createTodo , name='createTodo'),
    path('updatetodo/<int:id>/' ,updateTodo , name='updateTodo'),
    path('deletetodo/<int:id>/' ,deleteTodo , name='deleteTodo'),
]
