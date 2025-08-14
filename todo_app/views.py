# contacto/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DeleteView
from .models import Task, Contacto
from django.middleware.csrf import get_token
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_protect
import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone # Importar timezone si no lo tienes

# =======================================================
# VISTAS DE ADMINISTRACIÓN PROTEGIDAS
# =======================================================

@login_required
def admin_mensajes(request):
    """
    Vista que muestra todos los mensajes de contacto para la administración.
    Solo muestra los mensajes originales (que no son respuestas a otros).
    Protegida por @login_required.
    """
    mensajes = Contacto.objects.filter(respuesta_a__isnull=True).order_by('-fecha_envio')
    return render(request, 'todo_app/admin_mensajes.html', {'mensajes': mensajes})

@login_required
def marcar_como_leido(request, pk):
    """
    Marca un mensaje de contacto específico como leído y redirige a la página de administración.
    Protegida por @login_required.
    """
    mensaje = get_object_or_404(Contacto, pk=pk)
    if not mensaje.leido:
        mensaje.leido = True
        mensaje.save()
    return redirect('admin_mensajes')

class MensajeDeleteView(LoginRequiredMixin, DeleteView):
    """
    Vista genérica para eliminar un mensaje de contacto.
    Protegida por LoginRequiredMixin.
    """
    model = Contacto
    template_name = 'todo_app/mensaje_confirmar_borrar.html'
    success_url = reverse_lazy('admin_mensajes')

@login_required
def responder_mensaje(request, pk):
    """
    Vista para crear una respuesta a un mensaje de contacto.
    Crea un nuevo objeto de Contacto que está vinculado al mensaje original.
    """
    if request.method == 'POST':
        mensaje_original = get_object_or_404(Contacto, pk=pk)
        respuesta_texto = request.POST.get('respuesta_mensaje')

        if respuesta_texto:
            # Crea un nuevo objeto Contacto que es la respuesta
            nueva_respuesta = Contacto.objects.create(
                nombre="Administrador",
                email="admin@iconicastill.com", 
                mensaje=respuesta_texto,
                respuesta_a=mensaje_original, 
                leido=True 
            )
            
            # Opcionalmente, marca el mensaje original como leído
            mensaje_original.leido = True
            mensaje_original.save()
            
    return redirect('admin_mensajes')

# =======================================================
# VISTAS GENERALES (no requieren autenticación)
# =======================================================

def get_csrf_token(request):
    """
    Genera y devuelve un token CSRF.
    """
    token = get_token(request)
    return JsonResponse({'csrf_token': token})

@csrf_protect
def contacto(request):
    """
    Vista para el formulario de contacto.
    """
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

def index(request):
    """
    Vista para la página de inicio con la lista de tareas.
    """
    tasks = Task.objects.all()
    if request.method == "POST":
        title = request.POST.get('title')
        if title:
            Task.objects.create(title=title)
        return redirect('index')
    return render(request, 'todo_app/index.html', {'tasks': tasks})

def complete_task(request, task_id):
    """
    Vista para marcar una tarea como completada.
    """
    task = Task.objects.get(id=task_id)
    task.completed = not task.completed
    task.save()
    return redirect('index')

def delete_task(request, task_id):
    """
    Vista para eliminar una tarea.
    """
    task = Task.objects.get(id=task_id)
    task.delete()
    return redirect('index')

# ¡VISTA MODIFICADA!
def ver_mensajes(request):
    """
    Vista que muestra todos los mensajes de contacto de forma pública, 
    sin duplicados.
    """
    mensajes = Contacto.objects.filter(respuesta_a__isnull=True).order_by('-fecha_envio')
    return render(request, 'todo_app/mensajes.html', {'mensajes': mensajes})