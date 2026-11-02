from django.core.exceptions import ValidationError as DjangoValidationError
from django.utils import timezone
from rest_framework import serializers

from citas.models import Cita
from clientes.models import Cliente, Mascota
from servicios.models import Servicio


class ClienteSerializer(serializers.ModelSerializer):
    nombre_completo = serializers.CharField(read_only=True)
    total_mascotas = serializers.IntegerField(read_only=True, default=0)

    class Meta:
        model = Cliente
        fields = ("id", "nombres", "apellidos", "nombre_completo", "telefono", "email",
                  "direccion", "nit", "activo", "total_mascotas")


class MascotaSerializer(serializers.ModelSerializer):
    cliente_nombre = serializers.CharField(source="cliente.nombre_completo", read_only=True)
    especie_display = serializers.CharField(source="get_especie_display", read_only=True)
    edad = serializers.CharField(read_only=True)

    class Meta:
        model = Mascota
        fields = ("id", "cliente", "cliente_nombre", "nombre", "especie", "especie_display", "raza", "sexo",
                  "fecha_nacimiento", "edad", "color", "esterilizado", "notas", "activo")

    def validate_fecha_nacimiento(self, valor):
        if valor and valor > timezone.localdate():
            raise serializers.ValidationError("La fecha de nacimiento no puede estar en el futuro.")
        return valor


class ServicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servicio
        fields = ("id", "nombre", "descripcion", "precio", "duracion_minutos", "activo")


class CitaSerializer(serializers.ModelSerializer):
    mascota_nombre = serializers.CharField(source="mascota.nombre", read_only=True)
    cliente_nombre = serializers.CharField(source="mascota.cliente.nombre_completo", read_only=True)
    veterinario_nombre = serializers.CharField(source="veterinario.nombre_completo", read_only=True)
    servicio_nombre = serializers.CharField(source="servicio.nombre", read_only=True)
    estado_display = serializers.CharField(source="get_estado_display", read_only=True)
    fin = serializers.DateTimeField(read_only=True)
    estados_siguientes = serializers.SerializerMethodField()

    class Meta:
        model = Cita
        fields = ("id", "mascota", "mascota_nombre", "cliente_nombre", "veterinario", "veterinario_nombre",
                  "servicio", "servicio_nombre", "fecha_hora", "fin", "estado", "estado_display",
                  "estados_siguientes", "motivo")
        # El estado solo cambia con la acción /cambiar-estado/ (respeta las transiciones permitidas).
        read_only_fields = ("estado",)

    def get_estados_siguientes(self, cita):
        return [{"valor": e.value, "etiqueta": e.label} for e in cita.estados_siguientes]

    def validate(self, attrs):
        datos = super().validate(attrs)
        cita = self.instance or Cita()
        for campo, valor in datos.items():
            setattr(cita, campo, valor)

        nueva_fecha = datos.get("fecha_hora")
        if nueva_fecha and (not self.instance or nueva_fecha != self.instance.fecha_hora) and nueva_fecha <= timezone.now():
            raise serializers.ValidationError({"fecha_hora": "La cita debe ser en una fecha y hora futuras."})
        if self.instance and not self.instance.es_editable:
            raise serializers.ValidationError("Solo se pueden editar citas pendientes o confirmadas.")
        try:
            cita.clean()  # mismas reglas de negocio que el formulario web
        except DjangoValidationError as e:
            raise serializers.ValidationError(e.message_dict if hasattr(e, "error_dict") else e.messages)
        return datos


class CambiarEstadoSerializer(serializers.Serializer):
    estado = serializers.ChoiceField(choices=Cita.Estado.choices)
