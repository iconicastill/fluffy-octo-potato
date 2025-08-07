from django.shortcuts import render, redirect
from .models import Task, Contacto # Importa el nuevo modelo
from django.middleware.csrf import get_token
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_protect

def get_csrf_token(request):
    token = get_token(request)
    return JsonResponse({'csrf_token': token})

@csrf_protect
def contacto(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        telefono = request.POST.get('telefono')
        mensaje = request.POST.get('mensaje')

        # Guarda los datos en el nuevo modelo Contacto
        Contacto.objects.create(
            nombre=nombre,
            email=email,
            telefono=telefono,
            mensaje=mensaje
        )
        return JsonResponse({'status': 'success', 'message': 'Mensaje recibido. ¡Gracias!'})

    return HttpResponse("Este endpoint solo acepta peticiones POST.")

# Las vistas de Task se mantienen
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
