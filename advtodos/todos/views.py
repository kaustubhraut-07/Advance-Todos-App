
from .models import Todo
from .serializer import TodoSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from user.models import CustomUser

@api_view(['GET'])
def getallTodosforUser(request, email):
    try:
        user = CustomUser.objects.get(email=email)
    except CustomUser.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    todos = Todo.objects.filter(user=user)
    
    if todos.count() == 0:
        return Response([], status=status.HTTP_204_NO_CONTENT)
    else:
      
        serializer = TodoSerializer(todos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def createTodo(request,email):
    try:
        user = CustomUser.objects.get(email=email) 
    except CustomUser.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    title = request.data.get('title')
    description = request.data.get('description')
    completed = request.data.get('completed')
    todo = Todo.objects.create(user=user, title=title, description=description, completed=completed)
    serializer = TodoSerializer(todo)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['PUT'])
def updateTodo(request ,id):
    title = request.data.get('title')
    description = request.data.get('description')
    completed = request.data.get('completed')
    todo = Todo.objects.get(id=id)
    todo.title = title
    todo.description = description
    todo.completed = completed
    todo.save()
    serializer = TodoSerializer(todo)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['DELETE'])
def deleteTodo(request , id):
    todo = Todo.objects.get(id = id)
    print(todo , "todo that we are deleteing")
    todo.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)