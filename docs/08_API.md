# 8. API REST

Base: `/api/` · Formato: JSON · Paginación: 10 por página (`?page=2`) · Búsqueda: `?search=texto` · Orden: `?ordering=campo` (`-campo` descendente).

## Autenticación

| Método | Cómo |
|---|---|
| **Sesión** (la usa el frontend con `fetch`) | Cookie de sesión + cabecera `X-CSRFToken` en POST/PUT/PATCH/DELETE |
| **Token** (para otras apps / Postman) | `POST /api/token/` con `{"username": "...", "password": "..."}` → `{"token": "abc"}`; luego cabecera `Authorization: Token abc` |

Sin credenciales: `403`. Sin permiso por rol: `403`.

## Endpoints

| Método y ruta | Descripción | Lectura | Escritura |
|---|---|---|---|
| `GET/POST /api/clientes/` · `GET/PUT/PATCH/DELETE /api/clientes/{id}/` | Clientes. Filtro `?activo=true` | Todos | Admin, Recepción |
| `GET/POST /api/mascotas/` · `…/{id}/` | Mascotas. Filtros `?cliente=ID` `?especie=PERRO` `?activo=` | Todos | Admin, Recepción |
| `GET/POST /api/servicios/` · `…/{id}/` | Servicios | Todos | Admin |
| `GET/POST /api/citas/` · `GET/PUT/PATCH /api/citas/{id}/` | Citas. Filtros `?estado=` `?veterinario=ID` `?mascota=ID` `?fecha=2026-11-20` (sin DELETE: se cancelan) | Todos | Admin, Recepción |
| `POST /api/citas/{id}/cambiar-estado/` | Cuerpo `{"estado": "CONFIRMADA"}`; respeta las transiciones | — | Cualquier usuario autenticado |
| `GET /api/horarios-disponibles/?veterinario=1&servicio=2&fecha=2026-11-20[&cita=7]` | Horas libres (`["08:00","08:30",…]`) | Admin, Recepción | — |
| `GET /api/estadisticas/` | Indicadores y datos de gráficas | Todos | — |

## Códigos de respuesta

| Código | Significado |
|---|---|
| 200 / 201 / 204 | OK / creado / eliminado |
| 400 | Datos inválidos: el cuerpo trae los errores por campo, p. ej. `{"telefono": ["Ingresa un teléfono de 8 dígitos…"]}` |
| 403 | Sin sesión o sin permiso por rol |
| 404 | No existe |
| 405 | Método no permitido (p. ej. `DELETE` en citas) |
| 409 | No se puede eliminar porque tiene registros asociados |

## Ejemplos

```bash
# 1. Obtener token
curl -X POST http://localhost:8000/api/token/ -H "Content-Type: application/json" \
     -d '{"username":"recepcion","password":"Demo12345!"}'

# 2. Listar clientes que contengan "lopez"
curl "http://localhost:8000/api/clientes/?search=lopez" -H "Authorization: Token TU_TOKEN"

# 3. Crear una cita
curl -X POST http://localhost:8000/api/citas/ -H "Authorization: Token TU_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"mascota":1,"veterinario":3,"servicio":1,"fecha_hora":"2026-11-20T10:00:00-06:00","motivo":"Control"}'

# 4. Confirmarla
curl -X POST http://localhost:8000/api/citas/15/cambiar-estado/ -H "Authorization: Token TU_TOKEN" \
     -H "Content-Type: application/json" -d '{"estado":"CONFIRMADA"}'
```

En modo desarrollo (`DJANGO_DEBUG=True`) puedes explorar la API desde el navegador en <http://localhost:8000/api/>.

## Respuesta de ejemplo — `GET /api/citas/1/`

```json
{
  "id": 1,
  "mascota": 3, "mascota_nombre": "Rocky", "cliente_nombre": "José Ramírez",
  "veterinario": 3, "veterinario_nombre": "Ana Pérez",
  "servicio": 1, "servicio_nombre": "Consulta general",
  "fecha_hora": "2026-11-20T10:00:00-06:00", "fin": "2026-11-20T10:30:00-06:00",
  "estado": "PENDIENTE", "estado_display": "Pendiente",
  "estados_siguientes": [{"valor": "CONFIRMADA", "etiqueta": "Confirmada"}, {"valor": "CANCELADA", "etiqueta": "Cancelada"}],
  "motivo": "Control"
}
```
