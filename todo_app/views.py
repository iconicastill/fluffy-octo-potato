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
    
def ver_mensajes(request):
    # This is the new view for reading messages
    mensajes = Contacto.objects.all().order_by('-fecha_envio')
    return render(request, 'todo_app/mensajes.html', {'mensajes': mensajes})


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
