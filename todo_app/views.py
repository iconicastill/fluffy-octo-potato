# contacto/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DeleteView
from .models import Task, Contacto
from django.middleware.csrf import get_token
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_protect
import json
#login
from django.contrib.auth.decorators import login_required

# Tus vistas existentes

#login
@login_required
def admin_mensajes(request):
    mensajes = Contacto.objects.all().order_by('-fecha_envio')
    return render(request, 'todo_app/admin_mensajes.html', {'mensajes': mensajes})

@login_required
def marcar_como_leido(request, pk):
    """
    Marca un mensaje de contacto específico como leído y redirige a la página de administración.
    """
    mensaje = get_object_or_404(Contacto, pk=pk)
    if not mensaje.leido:
        mensaje.leido = True
        mensaje.save()
    return redirect('admin_mensajes')
    
# =======================================================
def get_csrf_token(request):
    token = get_token(request)
    return JsonResponse({'csrf_token': token})

@csrf_protect
def contacto(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            nombre = data.get('nombre')
            email = data.get('email')
            telefono = data.get('telefono')
            mensaje = data.get('mensaje')

            Contacto.objects.create(
                nombre=nombre,
                email=email,
                telefono=telefono,
                mensaje=mensaje
            )
            return JsonResponse({'status': 'success', 'message': 'Mensaje recibido. ¡Gracias!'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'error': 'Este endpoint solo acepta peticiones POST.'}, status=405)

# Las vistas de Task se mantienen igual
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
# =======================================================

def ver_mensajes(request):
    """
    Vista que muestra todos los mensajes de contacto de forma pública.
    """
    mensajes = Contacto.objects.all().order_by('-fecha_envio')
    return render(request, 'todo_app/mensajes.html', {'mensajes': mensajes})

# Vistas para la administración de mensajes
# =======================================================
def admin_mensajes(request):
    """
    Vista que muestra todos los mensajes de contacto para la administración.
    """
    mensajes = Contacto.objects.all().order_by('-fecha_envio')
    return render(request, 'todo_app/admin_mensajes.html', {'mensajes': mensajes})

def marcar_como_leido(request, pk):
    """
    Marca un mensaje de contacto específico como leído y redirige a la página de administración.
    """
    mensaje = get_object_or_404(Contacto, pk=pk)
    if not mensaje.leido:
        mensaje.leido = True
        mensaje.save()
    return redirect('admin_mensajes')

class MensajeDeleteView(DeleteView):
    """
    Vista genérica para eliminar un mensaje de contacto.
    """
    model = Contacto
    template_name = 'todo_app/mensaje_confirmar_borrar.html'
    success_url = reverse_lazy('admin_mensajes')
# =======================================================