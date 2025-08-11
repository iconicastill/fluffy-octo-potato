from django.db import models

class Task(models.Model):
    title = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title

# Nuevo modelo para el formulario de contacto
class Contacto(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    telefono = models.CharField(max_length=20, blank=True, null=True)
    mensaje = models.TextField()
    fecha_envio = models.DateTimeField(auto_now_add=True)

     # Nuevo campo para marcar el mensaje como leído
    leido = models.BooleanField(default=False)
    
    # Nuevo campo para vincular respuestas al mensaje original
    # Es un ForeignKey a sí mismo, permitiendo crear un hilo de conversación.
    respuesta_a = models.ForeignKey(
        'self', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='respuestas'
    )

    def __str__(self):
        return f"Mensaje de {self.nombre}"
