# tasks/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Task
from .serializers import TaskSerializer
from .forms import TaskForm
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

# API Views for RESTful endpoints
class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

@api_view(['GET', 'POST'])
def task_list_api(request):
    if request.method == 'GET':
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

@api_view(['GET', 'PUT', 'DELETE'])
def task_detail_api(request, pk):
    task = get_object_or_404(Task, pk=pk)
    
    if request.method == 'GET':
        serializer = TaskSerializer(task)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
    elif request.method == 'DELETE':
        task.delete()
        return Response(status=204)

# Frontend Views with Templates
def task_list(request):
    # Update the status of overdue tasks automatically
    tasks = Task.objects.all()
    updated_count = 0
    updated_task_ids = []
    
    for task in tasks:
        if task.is_overdue() and task.status not in ['DONE', 'MISSING']:
            task.status = 'MISSING'
            task.save(update_fields=['status'])
            updated_count += 1
            updated_task_ids.append(task.id)
    
    if updated_count > 0:
        messages.warning(request, f'{updated_count} task(s) marked as missing deadline!')
    
    tasks = Task.objects.all().order_by('-created_at')
    
    # Count tasks by status
    todo_count = Task.objects.filter(status='TODO').count()
    in_progress_count = Task.objects.filter(status='IN_PROGRESS').count()
    completed_count = Task.objects.filter(status='DONE').count()
    missing_count = Task.objects.filter(status='MISSING').count()
    
    context = {
        'tasks': tasks,
        'todo_count': todo_count,
        'in_progress_count': in_progress_count,
        'completed_count': completed_count,
        'missing_count': missing_count,
        'updated_task_ids': updated_task_ids,
    }
    return render(request, 'tasks/task_list.html', context)

def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    context = {'task': task}
    return render(request, 'tasks/task_detail.html', context)

def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task created successfully!')
            return redirect('task_list')
    else:
        form = TaskForm()
    
    context = {'form': form, 'is_create': True}
    return render(request, 'tasks/task_form.html', context)

def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)
    
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task updated successfully!')
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    
    context = {'form': form, 'task': task, 'is_create': False}
    return render(request, 'tasks/task_form.html', context)

def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    
    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Task deleted successfully!')
        return redirect('task_list')
    
    context = {'task': task}
    return render(request, 'tasks/task_confirm_delete.html', context)

@require_POST
def task_complete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.status = 'DONE'
    task.save()
    messages.success(request, 'Task marked as completed!')
    
    # Redirect back to the referring page, or to task list if no referrer
    if request.META.get('HTTP_REFERER'):
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect('task_list')

def task_reschedule(request, pk):
    task = get_object_or_404(Task, pk=pk)
    
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            task = form.save(commit=False)
            # If task was marked as missing, revert to its previous state
            if task.status == 'MISSING':
                task.status = 'TODO'
            task.save()
            messages.success(request, 'Task rescheduled successfully!')
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    
    context = {'form': form, 'task': task, 'is_reschedule': True}
    return render(request, 'tasks/task_form.html', context)

