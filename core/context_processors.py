from django.conf import settings


def negocio(request):
    """Datos del negocio y permisos de interfaz disponibles en todas las plantillas."""
    usuario = request.user
    autenticado = usuario.is_authenticated
    return {
        "NEGOCIO_NOMBRE": settings.NEGOCIO_NOMBRE,
        "NEGOCIO_TELEFONO": settings.NEGOCIO_TELEFONO,
        "NEGOCIO_DIRECCION": settings.NEGOCIO_DIRECCION,
        # Solo controlan qué botones se muestran; la seguridad real se aplica en las vistas.
        "puede_gestionar": autenticado and (usuario.es_admin or usuario.es_recepcion),   # clientes, mascotas, citas
        "puede_atender": autenticado and (usuario.es_admin or usuario.es_veterinario),   # consultas, vacunas
    }
