
from .models import Todo
from .serializer import TodoSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from user.models import CustomUser

@api_view(['GET'])
def getallTodosforUser(request):
    userId = request.param.get('id')
    todos = Todo.objects.filter(user=userId)
    if todos.count() == 0:
        return Response([], status=status.HTTP_204_NO_CONTENT)
    else:
        serializer = TodoSerializer(todos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def createTodo(request,id):
    try:
        user = CustomUser.objects.get(id=id) 
    except CustomUser.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    title = request.data.get('title')
    description = request.data.get('description')
    completed = request.data.get('completed')
    todo = Todo.objects.create(user=user, title=title, description=description, completed=completed)
    serializer = TodoSerializer(todo)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['PUT'])
def updateTodo(request):
    todoId = request.param.get('id')
    title = request.data.get('title')
    description = request.data.get('description')
    completed = request.data.get('completed')
    todo = Todo.objects.get(id=todoId)
    todo.title = title
    todo.description = description
    todo.completed = completed
    todo.save()
    serializer = TodoSerializer(todo)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['DELETE'])
def deleteTodo(request):
    todoId = request.param.get('id')
    todo = Todo.objects.get(id=todoId)
    todo.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)