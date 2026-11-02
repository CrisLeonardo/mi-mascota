from datetime import date

from django.core.exceptions import ValidationError as DjangoValidationError
from django.db.models import Count, ProtectedError
from django.utils import timezone
from rest_framework import mixins, serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import Usuario
from accounts.permissions import ADMIN, ADMIN_RECEPCION, TODOS, RolPermiso
from citas.models import Cita, horarios_disponibles
from clientes.models import Cliente, Mascota
from core import estadisticas
from servicios.models import Servicio

from .serializers import (
    CambiarEstadoSerializer,
    CitaSerializer,
    ClienteSerializer,
    MascotaSerializer,
    ServicioSerializer,
)


class ProtegidoDestroyMixin:
    """DELETE responde 409 (conflicto) si el registro tiene datos relacionados."""

    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except ProtectedError:
            return Response(
                {"detail": "No se puede eliminar: tiene registros asociados. Desactívalo en su lugar."},
                status=status.HTTP_409_CONFLICT,
            )


def _filtro_activo(qs, request):
    """?activo=true|false (si se omite, devuelve todos)."""
    valor = request.query_params.get("activo")
    if valor in ("true", "false"):
        qs = qs.filter(activo=(valor == "true"))
    return qs


class ClienteViewSet(ProtegidoDestroyMixin, viewsets.ModelViewSet):
    serializer_class = ClienteSerializer
    permission_classes = [RolPermiso]
    roles_lectura, roles_escritura = TODOS, ADMIN_RECEPCION
    search_fields = ("nombres", "apellidos", "telefono", "email", "nit")
    ordering_fields = ("apellidos", "nombres", "id")

    def get_queryset(self):
        qs = Cliente.objects.annotate(total_mascotas=Count("mascotas")).order_by("apellidos", "nombres")
        return _filtro_activo(qs, self.request)


class MascotaViewSet(ProtegidoDestroyMixin, viewsets.ModelViewSet):
    serializer_class = MascotaSerializer
    permission_classes = [RolPermiso]
    roles_lectura, roles_escritura = TODOS, ADMIN_RECEPCION
    search_fields = ("nombre", "raza", "cliente__nombres", "cliente__apellidos")
    ordering_fields = ("nombre", "id")

    def get_queryset(self):
        qs = Mascota.objects.select_related("cliente")
        params = self.request.query_params
        if params.get("cliente", "").isdigit():
            qs = qs.filter(cliente_id=params["cliente"])
        if params.get("especie") in Mascota.Especie.values:
            qs = qs.filter(especie=params["especie"])
        return _filtro_activo(qs, self.request)


class ServicioViewSet(ProtegidoDestroyMixin, viewsets.ModelViewSet):
    serializer_class = ServicioSerializer
    permission_classes = [RolPermiso]
    roles_lectura, roles_escritura = TODOS, ADMIN
    queryset = Servicio.objects.all()
    search_fields = ("nombre",)

    def get_queryset(self):
        return _filtro_activo(super().get_queryset(), self.request)


class CitaViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    """Citas. No se exponen borrados: una cita se cancela, no se elimina."""

    serializer_class = CitaSerializer
    permission_classes = [RolPermiso]
    roles_lectura, roles_escritura = TODOS, ADMIN_RECEPCION
    search_fields = ("mascota__nombre", "mascota__cliente__nombres", "mascota__cliente__apellidos")
    ordering_fields = ("fecha_hora", "id")

    def get_queryset(self):
        qs = Cita.objects.select_related("mascota", "mascota__cliente", "veterinario", "servicio")
        p = self.request.query_params
        if p.get("estado") in Cita.Estado.values:
            qs = qs.filter(estado=p["estado"])
        if p.get("veterinario", "").isdigit():
            qs = qs.filter(veterinario_id=p["veterinario"])
        if p.get("mascota", "").isdigit():
            qs = qs.filter(mascota_id=p["mascota"])
        if p.get("fecha"):
            try:
                qs = qs.filter(fecha_hora__date=date.fromisoformat(p["fecha"]))
            except ValueError:
                qs = qs.none()
        return qs

    def perform_create(self, serializer):
        self._guardar(serializer, creado_por=self.request.user)

    def perform_update(self, serializer):
        self._guardar(serializer)

    @staticmethod
    def _guardar(serializer, **extra):
        # Cita.save() revisa otra vez los traslapes con la fila bloqueada (condición de carrera).
        try:
            serializer.save(**extra)
        except DjangoValidationError as error:
            raise serializers.ValidationError(error.message_dict)

    @action(detail=True, methods=["post"], url_path="cambiar-estado", permission_classes=[IsAuthenticated])
    def cambiar_estado(self, request, pk=None):
        """Cambia el estado respetando Cita.TRANSICIONES. Lo usan los botones de la lista (fetch)."""
        cita = self.get_object()
        entrada = CambiarEstadoSerializer(data=request.data)
        entrada.is_valid(raise_exception=True)
        nuevo = entrada.validated_data["estado"]
        if not cita.puede_pasar_a(nuevo):
            return Response(
                {"detail": f"No se puede pasar de «{cita.get_estado_display()}» a «{Cita.Estado(nuevo).label}»."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        cita.estado = nuevo
        cita.save(update_fields=["estado"])
        return Response(self.get_serializer(cita).data)


class HorariosDisponiblesView(APIView):
    """GET /api/horarios-disponibles/?veterinario=1&fecha=2026-11-20&servicio=3[&cita=7]"""

    permission_classes = [RolPermiso]
    roles_lectura = ADMIN_RECEPCION

    def get(self, request):
        p = request.query_params
        try:
            fecha = date.fromisoformat(p.get("fecha", ""))
            veterinario = Usuario.objects.get(pk=p.get("veterinario"), rol=Usuario.Rol.VETERINARIO, is_active=True)
            servicio = Servicio.objects.get(pk=p.get("servicio"), activo=True)
        except (ValueError, TypeError, Usuario.DoesNotExist, Servicio.DoesNotExist):
            return Response({"detail": "Parámetros inválidos: fecha, veterinario y servicio."}, status=400)
        excluir = int(p["cita"]) if p.get("cita", "").isdigit() else None
        libres = horarios_disponibles(veterinario, fecha, servicio.duracion_minutos, excluir_cita_id=excluir)
        return Response({
            "fecha": fecha.isoformat(),
            "duracion_minutos": servicio.duracion_minutos,
            "horarios": [timezone.localtime(h).strftime("%H:%M") for h in libres],
        })


class EstadisticasView(APIView):
    """Datos del dashboard (los consume Chart.js con fetch)."""

    permission_classes = [RolPermiso]
    roles_lectura = TODOS

    def get(self, request):
        return Response({
            "resumen": estadisticas.resumen(),
            "citas_por_estado": estadisticas.citas_por_estado(),
            "citas_proximos_dias": estadisticas.citas_proximos_dias(),
        })
