# 3. Diagrama Entidad-Relación

> GitHub dibuja este diagrama automáticamente. Para obtener una **imagen PNG/SVG** para el documento o la
> presentación, abre [`diagrama_er.html`](diagrama_er.html) en el navegador y haz una captura, o pega el código
> en <https://mermaid.live> y descarga la imagen.

```mermaid
erDiagram
    USUARIO ||--o{ CITA : "atiende (veterinario)"
    USUARIO ||--o{ CITA : "agenda (creado_por)"
    USUARIO ||--o{ CONSULTA : "realiza"
    USUARIO ||--o{ VACUNA : "aplica"
    CLIENTE ||--|{ MASCOTA : "es dueño de"
    MASCOTA ||--o{ CITA : "tiene"
    MASCOTA ||--o{ CONSULTA : "tiene"
    MASCOTA ||--o{ VACUNA : "recibe"
    SERVICIO ||--o{ CITA : "se presta en"
    CITA ||--o| CONSULTA : "origina"

    USUARIO {
        bigint id PK
        varchar username UK
        varchar password "hash"
        varchar first_name
        varchar last_name
        varchar email
        varchar rol "ADMIN | RECEPCION | VETERINARIO"
        varchar telefono
        boolean is_active
    }
    CLIENTE {
        bigint id PK
        varchar nombres
        varchar apellidos
        varchar telefono
        varchar email
        varchar direccion
        varchar nit
        boolean activo
        datetime creado
    }
    MASCOTA {
        bigint id PK
        bigint cliente_id FK
        varchar nombre
        varchar especie "PERRO|GATO|AVE|ROEDOR|REPTIL|OTRO"
        varchar raza
        char sexo "M | H"
        date fecha_nacimiento
        varchar color
        boolean esterilizado
        text notas
        boolean activo
    }
    SERVICIO {
        bigint id PK
        varchar nombre UK
        text descripcion
        decimal precio
        smallint duracion_minutos
        boolean activo
    }
    CITA {
        bigint id PK
        bigint mascota_id FK
        bigint veterinario_id FK
        bigint servicio_id FK
        bigint creado_por_id FK
        datetime fecha_hora
        smallint duracion_minutos
        varchar estado "PENDIENTE|CONFIRMADA|ATENDIDA|CANCELADA|NO_ASISTIO"
        text motivo
        datetime creado
    }
    CONSULTA {
        bigint id PK
        bigint mascota_id FK
        bigint cita_id FK "UK, opcional"
        bigint veterinario_id FK
        datetime fecha
        decimal peso_kg
        decimal temperatura_c
        text sintomas
        text diagnostico
        text tratamiento
        text observaciones
        decimal costo
    }
    VACUNA {
        bigint id PK
        bigint mascota_id FK
        bigint aplicada_por_id FK
        varchar nombre
        date fecha_aplicacion
        date proxima_dosis
        varchar lote
        varchar notas
    }
```

## Relaciones y reglas de integridad

| Relación | Cardinalidad | `on_delete` | Por qué |
|---|---|---|---|
| Cliente → Mascota | 1 : N (un cliente tiene 1 o más mascotas) | `PROTECT` | No se borra un dueño con mascotas registradas. |
| Mascota → Cita / Consulta / Vacuna | 1 : N | `PROTECT` | El historial clínico no se pierde al borrar por error. |
| Usuario (veterinario) → Cita / Consulta | 1 : N | `PROTECT` | Se conserva quién atendió. Los usuarios se **desactivan**, no se borran. |
| Servicio → Cita | 1 : N | `PROTECT` | No se borra un servicio que ya se usó. |
| Cita → Consulta | 1 : 0..1 | `SET_NULL` | Una cita se atiende una sola vez; una consulta puede existir sin cita (urgencia). |
| Usuario → Cita (`creado_por`), Vacuna (`aplicada_por`) | 1 : N | `SET_NULL` | Trazabilidad opcional. |

## Diccionario de datos (resumen)

**usuario** — extiende `AbstractUser` de Django. `rol` define los permisos. Se desactiva con `is_active=False`.

**cliente** — propietario. `telefono` valida 8 dígitos (`2222-3333`). Índice por `(apellidos, nombres)` para búsquedas.

**mascota** — paciente. `edad` se calcula (no se guarda) a partir de `fecha_nacimiento`.

**servicio** — catálogo. `duracion_minutos` determina cuántos "espacios" ocupa una cita en la agenda.

**cita** — `duracion_minutos` se copia del servicio al guardar, para que cambiar el servicio después no mueva
citas ya agendadas. Índices por `fecha_hora` y `(veterinario, fecha_hora)` aceleran el cálculo de horarios libres.

**consulta** — registro clínico; `costo` toma por defecto el precio del servicio de la cita.

**vacuna** — `proxima_dosis` permite listar refuerzos vencidos o próximos (índice propio).

## Normalización

El modelo está en **3FN**: no hay atributos repetidos (los datos del dueño viven en `cliente`, no en `mascota`),
cada atributo depende de la clave de su tabla y los valores calculados (edad, fin de cita, nombre completo) no se almacenan.
La única copia deliberada es `cita.duracion_minutos` (desnormalización controlada, explicada arriba).
