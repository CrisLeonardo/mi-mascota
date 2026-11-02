"""
Crea (o actualiza) el administrador inicial a partir de variables de entorno.

    DJANGO_ADMIN_USER=admin DJANGO_ADMIN_PASSWORD=... python manage.py crear_admin

Sirve para el despliegue en hostings gratuitos que no ofrecen terminal (Render):
se ejecuta en cada build y es idempotente.
"""
import os

from django.core.management.base import BaseCommand

from accounts.models import Usuario


class Command(BaseCommand):
    help = "Crea el usuario administrador usando DJANGO_ADMIN_USER / DJANGO_ADMIN_PASSWORD / DJANGO_ADMIN_EMAIL."

    def handle(self, *args, **options):
        usuario = os.getenv("DJANGO_ADMIN_USER")
        password = os.getenv("DJANGO_ADMIN_PASSWORD")
        if not (usuario and password):
            self.stdout.write("DJANGO_ADMIN_USER / DJANGO_ADMIN_PASSWORD no definidas: no se crea administrador.")
            return
        admin, creado = Usuario.objects.get_or_create(
            username=usuario,
            defaults={"email": os.getenv("DJANGO_ADMIN_EMAIL", ""), "rol": Usuario.Rol.ADMIN,
                      "is_staff": True, "is_superuser": True, "first_name": "Administrador"},
        )
        if creado:
            admin.set_password(password)
            admin.save()
            self.stdout.write(self.style.SUCCESS(f"Administrador '{usuario}' creado."))
        else:
            self.stdout.write(f"El administrador '{usuario}' ya existe; no se modifica.")
