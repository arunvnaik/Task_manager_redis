from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.cache import cache
from django.shortcuts import get_object_or_404
from .models import Task, Project
from .serializers import TaskSerializer, ProjectSerializer
from rest_framework.permissions import IsAuthenticated

# TaskList handles listing all tasks and creating new tasks
class TaskList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Attempt to retrieve cached tasks
        serialized_tasks = cache.get('tasks')
        if serialized_tasks is None:  # Consistent None checking
            tasks = Task.objects.all()
            serialized_tasks = TaskSerializer(tasks, many=True).data
            cache.set('tasks', serialized_tasks, timeout=60*15)
        
        return Response(serialized_tasks, status=status.HTTP_200_OK)

    def post(self, request):
        # Create a new task and invalidate cache
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            cache.delete('tasks')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# TaskDetail handles retrieving, updating, and deleting a specific task
class TaskDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        # Attempt to retrieve task from cache
        task_data = cache.get(f'task_{pk}')
        if task_data is None:  # Consistent None checking
            task = get_object_or_404(Task, pk=pk)
            task_data = TaskSerializer(task).data
            cache.set(f'task_{pk}', task_data, timeout=60*15)
        return Response(task_data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        # Update task and invalidate cache
        task = get_object_or_404(Task, pk=pk)
        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            cache.delete(f'task_{pk}')
            cache.delete('tasks')
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        # Delete task and clear cache
        task = get_object_or_404(Task, pk=pk)
        task.delete()
        cache.delete(f'task_{pk}')
        cache.delete('tasks')
        return Response(status=status.HTTP_204_NO_CONTENT)

# ProjectList handles listing all projects and creating new projects
class ProjectList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Attempt to retrieve cached projects
        serialized_projects = cache.get('projects')
        if serialized_projects is None:  # Consistent None checking
            projects = Project.objects.all()
            serialized_projects = ProjectSerializer(projects, many=True).data
            cache.set('projects', serialized_projects, timeout=60*15)
        
        return Response(serialized_projects, status=status.HTTP_200_OK)

    def post(self, request):
        # Create a new project and invalidate cache
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            cache.delete('projects')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ProjectDetail handles retrieving, updating, and deleting a specific project
class ProjectDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        # Attempt to retrieve project from cache
        project_data = cache.get(f'project_{pk}')
        if project_data is None:  # Consistent None checking
            project = get_object_or_404(Project, pk=pk)
            project_data = ProjectSerializer(project).data
            cache.set(f'project_{pk}', project_data, timeout=60*15)
        return Response(project_data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        # Update project and invalidate cache
        project = get_object_or_404(Project, pk=pk)
        serializer = ProjectSerializer(project, data=request.data)
        if serializer.is_valid():
            serializer.save()
            cache.delete(f'project_{pk}')
            cache.delete('projects')
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        # Delete project and clear cache
        project = get_object_or_404(Project, pk=pk)
        project.delete()
        cache.delete(f'project_{pk}')
        cache.delete('projects')
        return Response(status=status.HTTP_204_NO_CONTENT)
