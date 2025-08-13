import os
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Sets the admin password from an environment variable.'

    def handle(self, *args, **kwargs):
        # Obtener el nombre de usuario y la nueva contraseña de las variables de entorno
        username = 'admin'
        password = os.environ.get('ADMIN_PASSWORD')

        if not password:
            self.stdout.write(self.style.ERROR('ADMIN_PASSWORD environment variable not set.'))
            return

        try:
            # Buscar el usuario y actualizar la contraseña
            user = User.objects.get(username=username)
            user.set_password(password)
            user.save()
            self.stdout.write(self.style.SUCCESS(f'Password for user "{username}" has been successfully set.'))
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'User "{username}" does not exist.'))