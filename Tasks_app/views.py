from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.cache import cache
from django.shortcuts import get_object_or_404
from .models import Task, Project
from .serializers import TaskSerializer, ProjectSerializer

class TaskList(APIView):
    def get(self, request):
        cached_tasks = cache.get('tasks')
        if cached_tasks is not None:
            tasks = cached_tasks
        else:
            tasks = Task.objects.all()
            serialized_tasks = TaskSerializer(tasks, many=True).data
            cache.set('tasks', serialized_tasks, timeout=60*15)
        
        return Response(serialized_tasks, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            cache.delete('tasks')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TaskDetail(APIView):
    def get(self, request, pk):
        task = cache.get(f'task_{pk}')
        if not task:
            task = get_object_or_404(Task, pk=pk)
            task_data = TaskSerializer(task).data
            cache.set(f'task_{pk}', task_data, timeout=60*15)
        return Response(task_data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            cache.delete(f'task_{pk}')
            cache.delete('tasks')
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        task.delete()
        cache.delete(f'task_{pk}')
        cache.delete('tasks')
        return Response(status=status.HTTP_204_NO_CONTENT)

# class ProjectList(APIView):
  
class ProjectList(APIView):
    def get(self, request):
        cached_projects = cache.get('projects')
        if cached_projects is not None:
            projects = cached_projects
        else:
            projects = Project.objects.all()
            serialized_projects = ProjectSerializer(projects, many=True).data
            cache.set('projects', serialized_projects, timeout=60*15)
        
        return Response(projects)

    def post(self, request):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            cache.delete('projects')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProjectDetail(APIView):
    def get(self, request, pk):
        project_data = cache.get(f'project_{pk}')
        if not project_data:
            project = get_object_or_404(Project, pk=pk)
            project_data = ProjectSerializer(project).data
            cache.set(f'project_{pk}', project_data, timeout=60*15)
        return Response(project_data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        serializer = ProjectSerializer(project, data=request.data)
        if serializer.is_valid():
            serializer.save()
            cache.delete(f'project_{pk}')
            cache.delete('projects')
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        project.delete()
        cache.delete(f'project_{pk}')
        cache.delete('projects')
        return Response(status=status.HTTP_204_NO_CONTENT)
