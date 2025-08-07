from django.urls import path
from . import views

urlpatterns = [
    # URLs de la app de tareas
    path('', views.index, name='index'),
    path('complete/<int:task_id>/', views.complete_task, name='complete_task'),
    path('delete/<int:task_id>/', views.delete_task, name='delete_task'),

    # Nuevas URLs para el formulario de contacto
    path('get-csrf-token/', views.get_csrf_token, name='get_csrf_token'),
    path('contacto/', views.contacto, name='contacto'),
]
