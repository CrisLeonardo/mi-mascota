"""Consultas agregadas para el dashboard y para el endpoint /api/estadisticas/."""
from datetime import timedelta

from django.db.models import Count, Sum
from django.db.models.functions import TruncDate
from django.utils import timezone

from citas.models import Cita
from clientes.models import Cliente, Mascota
from expedientes.models import Consulta, Vacuna


def resumen():
    hoy = timezone.localdate()
    desde = hoy - timedelta(days=30)
    recientes = Consulta.objects.filter(fecha__date__gte=desde)
    ingresos = recientes.aggregate(total=Sum("costo"))["total"] or 0
    return {
        "citas_hoy": Cita.objects.filter(fecha_hora__date=hoy, estado__in=Cita.ESTADOS_ACTIVOS).count(),
        "citas_pendientes": Cita.objects.filter(estado=Cita.Estado.PENDIENTE, fecha_hora__date__gte=hoy).count(),
        "clientes": Cliente.objects.filter(activo=True).count(),
        "mascotas": Mascota.objects.filter(activo=True).count(),
        "consultas_30d": recientes.count(),
        "ingresos_30d": float(ingresos),
        "refuerzos_proximos": Vacuna.objects.filter(
            proxima_dosis__gte=hoy, proxima_dosis__lte=hoy + timedelta(days=30)
        ).count(),
    }


def citas_por_estado():
    conteo = dict(Cita.objects.values_list("estado").annotate(n=Count("id")))
    return [{"estado": etiqueta, "clave": clave, "total": conteo.get(clave, 0)} for clave, etiqueta in Cita.Estado.choices]


def citas_proximos_dias(dias=7):
    hoy = timezone.localdate()
    conteo = {
        fila["dia"]: fila["n"]
        for fila in Cita.objects.filter(
            estado__in=Cita.ESTADOS_ACTIVOS, fecha_hora__date__gte=hoy, fecha_hora__date__lt=hoy + timedelta(days=dias)
        )
        .values(dia=TruncDate("fecha_hora"))
        .annotate(n=Count("id"))
    }
    return [
        {"fecha": (hoy + timedelta(days=i)).isoformat(), "total": conteo.get(hoy + timedelta(days=i), 0)}
        for i in range(dias)
    ]
