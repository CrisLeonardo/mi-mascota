"""
Carga datos de demostración para probar y presentar el sistema.

    python manage.py seed_demo            # crea usuarios y datos de ejemplo
    python manage.py seed_demo --reset    # borra los datos de negocio y vuelve a crear

Usuarios de demostración (contraseña por defecto: Demo12345!):
    admin / recepcion / vet_ana / vet_luis
"""
import random
from datetime import datetime, time, timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from accounts.models import Usuario
from citas.models import Cita
from clientes.models import Cliente, Mascota
from expedientes.models import Consulta, Vacuna
from servicios.models import Servicio

CLIENTES = [
    ("María", "López", "5512-3456", "maria.lopez@example.com", "Zona 10, Ciudad de Guatemala"),
    ("José", "Ramírez", "4123-9087", "jose.ramirez@example.com", "Zona 1, Mixco"),
    ("Ana", "García", "5890-1122", "ana.garcia@example.com", "Villa Nueva"),
    ("Carlos", "Morales", "3344-7788", "", "Zona 7, Ciudad de Guatemala"),
    ("Lucía", "Hernández", "5566-0099", "lucia.h@example.com", "San Miguel Petapa"),
    ("Pedro", "Castillo", "4455-2210", "", "Zona 12, Ciudad de Guatemala"),
]

MASCOTAS = [  # (índice cliente, nombre, especie, raza, sexo, meses de edad, color)
    (0, "Max", "PERRO", "Labrador", "M", 48, "Dorado"),
    (0, "Luna", "GATO", "Siamés", "H", 30, "Crema"),
    (1, "Rocky", "PERRO", "Pastor Alemán", "M", 72, "Negro y café"),
    (2, "Nala", "PERRO", "Mestizo", "H", 18, "Café"),
    (2, "Tom", "GATO", "Mestizo", "M", 12, "Gris"),
    (3, "Kiwi", "AVE", "Perico", "M", 24, "Verde"),
    (4, "Bella", "PERRO", "Poodle", "H", 60, "Blanco"),
    (5, "Simba", "GATO", "Persa", "M", 36, "Naranja"),
]

SERVICIOS = [
    ("Consulta general", "Revisión médica general de la mascota.", 150, 30),
    ("Vacunación", "Aplicación de vacunas del esquema.", 120, 30),
    ("Desparasitación", "Desparasitación interna y externa.", 90, 30),
    ("Baño y corte", "Servicio de estética canina y felina.", 180, 60),
    ("Cirugía menor", "Procedimientos quirúrgicos ambulatorios.", 600, 90),
    ("Esterilización", "Cirugía de esterilización.", 800, 120),
]


class Command(BaseCommand):
    help = "Carga usuarios y datos de demostración."

    def add_arguments(self, parser):
        parser.add_argument("--reset", action="store_true", help="Borra los datos de negocio antes de cargar.")
        parser.add_argument("--password", default="Demo12345!", help="Contraseña de los usuarios de demo.")

    def handle(self, *args, **opts):
        if opts["reset"]:
            for modelo in (Consulta, Vacuna, Cita, Mascota, Cliente, Servicio):
                modelo.objects.all().delete()

        usuarios = self._crear_usuarios(opts["password"])
        servicios = [Servicio.objects.get_or_create(
            nombre=n, defaults={"descripcion": d, "precio": p, "duracion_minutos": m})[0] for n, d, p, m in SERVICIOS]
        clientes = [Cliente.objects.get_or_create(
            nombres=n, apellidos=a, defaults={"telefono": t, "email": e, "direccion": d})[0] for n, a, t, e, d in CLIENTES]

        hoy = timezone.localdate()
        mascotas = []
        for i, nombre, especie, raza, sexo, meses, color in MASCOTAS:
            nacimiento = hoy - timedelta(days=meses * 30)
            m, _ = Mascota.objects.get_or_create(
                cliente=clientes[i], nombre=nombre,
                defaults={"especie": especie, "raza": raza, "sexo": sexo, "fecha_nacimiento": nacimiento, "color": color},
            )
            mascotas.append(m)

        if not Cita.objects.exists():
            self._crear_citas(mascotas, servicios, usuarios)
        if not Vacuna.objects.exists():
            self._crear_vacunas(mascotas, usuarios["vet_ana"])

        self.stdout.write(self.style.SUCCESS(
            f"Datos de demo listos. Usuarios: admin, recepcion, vet_ana, vet_luis (contraseña: {opts['password']})"))

    def _crear_usuarios(self, password):
        definiciones = [
            ("admin", "Administrador", "General", Usuario.Rol.ADMIN, True),
            ("recepcion", "Rosa", "Mendoza", Usuario.Rol.RECEPCION, False),
            ("vet_ana", "Ana", "Pérez", Usuario.Rol.VETERINARIO, False),
            ("vet_luis", "Luis", "Solares", Usuario.Rol.VETERINARIO, False),
        ]
        usuarios = {}
        for username, nombre, apellido, rol, staff in definiciones:
            u, creado = Usuario.objects.get_or_create(
                username=username,
                defaults={"first_name": nombre, "last_name": apellido, "rol": rol,
                          "email": f"{username}@example.com", "is_staff": staff, "is_superuser": staff},
            )
            if creado:
                u.set_password(password)
                u.save()
            usuarios[username] = u
        return usuarios

    def _crear_citas(self, mascotas, servicios, usuarios):
        veterinarios = [usuarios["vet_ana"], usuarios["vet_luis"]]
        ahora = timezone.now()
        hoy = timezone.localdate()
        rnd = random.Random(7)

        def en(dia_offset, hora, minuto=0):
            dia = hoy + timedelta(days=dia_offset)
            while dia.weekday() == 6:  # sin domingos
                dia += timedelta(days=1)
            return timezone.make_aware(datetime.combine(dia, time(hora, minuto)))

        # Citas pasadas ya atendidas, con su consulta.
        for k, dia in enumerate((-12, -9, -6, -3, -2)):
            masc = mascotas[k % len(mascotas)]
            vet = veterinarios[k % 2]
            serv = servicios[0]
            cita = Cita.objects.create(
                mascota=masc, veterinario=vet, servicio=serv, fecha_hora=en(dia, 9 + k),
                estado=Cita.Estado.ATENDIDA, motivo="Control general", creado_por=usuarios["recepcion"],
            )
            Consulta.objects.create(
                mascota=masc, cita=cita, veterinario=vet, fecha=cita.fecha_hora,
                peso_kg=round(rnd.uniform(3, 30), 2), temperatura_c=round(rnd.uniform(38, 39.5), 1),
                sintomas="Revisión de rutina, sin molestias.", diagnostico="Paciente sano.",
                tratamiento="Continuar con alimentación balanceada.", costo=serv.precio,
            )

        # Citas de hoy y próximos días.
        futuras = [(0, 15, 0), (0, 16, 0), (1, 9, 0), (1, 10, 30), (2, 11, 0), (3, 14, 0), (4, 9, 30), (5, 15, 30)]
        for k, (dia, hora, minuto) in enumerate(futuras):
            inicio = en(dia, hora, minuto)
            if inicio <= ahora:
                inicio = en(dia + 7, hora, minuto)
            try:
                Cita.objects.create(
                    mascota=mascotas[(k + 2) % len(mascotas)], veterinario=veterinarios[k % 2],
                    servicio=servicios[k % 3], fecha_hora=inicio,
                    estado=Cita.Estado.CONFIRMADA if k % 2 == 0 else Cita.Estado.PENDIENTE,
                    motivo="Cita agendada por teléfono.", creado_por=usuarios["recepcion"],
                )
            except Exception:  # un choque de horario no debe detener la carga de demo
                continue

    def _crear_vacunas(self, mascotas, vet):
        hoy = timezone.localdate()
        datos = [
            (mascotas[0], "Antirrábica", -200, 165),
            (mascotas[0], "Parvovirus", -100, 265),
            (mascotas[2], "Antirrábica", -340, 25),   # refuerzo próximo
            (mascotas[3], "Quíntuple", -60, 20),      # refuerzo próximo
            (mascotas[1], "Triple felina", -300, -5),  # refuerzo vencido
        ]
        for masc, nombre, aplicada, refuerzo in datos:
            Vacuna.objects.create(
                mascota=masc, nombre=nombre, fecha_aplicacion=hoy + timedelta(days=aplicada),
                proxima_dosis=hoy + timedelta(days=refuerzo), aplicada_por=vet,
            )
