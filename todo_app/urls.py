# todo_app/urls.py

from django.urls import path
from . import views
from .views import MensajeDeleteView

urlpatterns = [
    # URLs de la app de tareas (sin cambios)
    path('', views.index, name='index'),
    path('complete/<int:task_id>/', views.complete_task, name='complete_task'),
    path('delete/<int:task_id>/', views.delete_task, name='delete_task'),

    # Nuevas URLs para el formulario de contacto (sin cambios)
    path('get-csrf-token/', views.get_csrf_token, name='get_csrf_token'),
    path('contacto/', views.contacto, name='contacto'),
    
    # URL para los mensajes públicos (nueva vista)
    path('mensajes/', views.ver_mensajes, name='ver_mensajes'),
    
    # URL de la vista de administración
    path('admin/mensajes/', views.admin_mensajes, name='admin_mensajes'),
    
    # Nuevas URLs para las funcionalidades de administración
    path('admin/marcar-leido/<int:pk>/', views.marcar_como_leido, name='marcar_como_leido'),
    path('admin/borrar/<int:pk>/', MensajeDeleteView.as_view(), name='mensaje_borrar'),
]