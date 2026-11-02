from django.core.validators import RegexValidator

# Teléfonos de Guatemala: 8 dígitos, con o sin guion (2222-3333 / 22223333).
validar_telefono = RegexValidator(
    regex=r"^\d{4}-?\d{4}$",
    message="Ingresa un teléfono de 8 dígitos, por ejemplo 2222-3333.",
)
