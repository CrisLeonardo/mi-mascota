from django import template

register = template.Library()

_CLASES_ESTADO = {
    "PENDIENTE": "text-bg-warning",
    "CONFIRMADA": "text-bg-info",
    "ATENDIDA": "text-bg-success",
    "CANCELADA": "text-bg-secondary",
    "NO_ASISTIO": "text-bg-danger",
}


@register.filter
def clase_estado(valor):
    """Clase de Bootstrap para el badge de estado de una cita."""
    return _CLASES_ESTADO.get(valor, "text-bg-light")


@register.filter
def icono_especie(valor):
    return {
        "PERRO": "bi-emoji-smile", "GATO": "bi-emoji-sunglasses", "AVE": "bi-feather",
        "ROEDOR": "bi-bug", "REPTIL": "bi-water", "OTRO": "bi-question-circle",
    }.get(valor, "bi-question-circle")
