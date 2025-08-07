from django.shortcuts import render, redirect
from .models import Task
from django.middleware.csrf import get_token
from django.http import JsonResponse

def get_csrf_token(request):
    token = get_token(request)
    return JsonResponse({'csrf_token': token})

def index(request):
    tasks = Task.objects.all()
    if request.method == "POST":
        title = request.POST.get('title')
        if title:
            Task.objects.create(title=title)
        return redirect('index')
    return render(request, 'todo_app/index.html', {'tasks': tasks})

def complete_task(request, task_id):
    task = Task.objects.get(id=task_id)
    task.completed = not task.completed
    task.save()
    return redirect('index')

def delete_task(request, task_id):
    task = Task.objects.get(id=task_id)
    task.delete()
    return redirect('index')
