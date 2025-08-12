from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')), # <-- Esto activa las urls de login y logout
    path('', include('todo_app.urls')),
]
