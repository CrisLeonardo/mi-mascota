# 6. Plan de pruebas

## 1. Pruebas automáticas (67)

```bash
python manage.py test                 # todas
python manage.py test citas           # solo una app
python manage.py test citas.tests.CitaModeloTests.test_no_permite_traslape_del_veterinario   # una prueba
```

| Archivo | Qué verifica |
|---|---|
| `accounts/tests.py` | Login/logout, usuario inactivo, **matriz de permisos por rol**, crear usuarios, no auto-desactivarse |
| `clientes/tests.py` | Validación de teléfono, CRUD, **no borrar con datos relacionados**, búsqueda, paginación, respuesta parcial (AJAX), filtro de inactivos, edad de mascotas |
| `citas/tests.py` | Duración y fin, **traslapes**, citas consecutivas, citas canceladas liberan horario, fuera de horario, rol del veterinario, transiciones de estado, **cálculo de horarios libres**, domingos, formulario, **reserva simultánea** (re-validación al guardar; la prueba con dos hilos solo corre en PostgreSQL) |
| `expedientes/tests.py` | Atender cita → consulta + cita "atendida" (transacción), cita cancelada no se atiende, consulta sin cita, rangos de temperatura, vacunas y refuerzos |
| `servicios/tests.py` | Alta de servicios solo admin, precio negativo, nombre único, no borrar servicios usados |
| `api/tests.py` | Autenticación (sesión y token), permisos por rol, CRUD y validaciones, **409 al borrar con relaciones**, cambio de estado con transiciones, filtros, horarios libres, estadísticas, horario ocupado entre validar y guardar → 400 |

Las pruebas corren en cada push y Pull Request mediante **GitHub Actions** (`.github/workflows/ci.yml`).

### Cómo está escrita una prueba (ejemplo)

```python
def test_no_permite_traslape_del_veterinario(self):
    crear_cita(self, 10, 0)                       # Arrange: ya hay una cita 10:00-10:30
    otra = Cita(mascota=self.mascota, veterinario=self.vet,
                servicio=self.servicio, fecha_hora=fecha_hora(10, 15))
    with self.assertRaises(ValidationError):      # Act + Assert: la nueva debe rechazarse
        otra.full_clean()
```

## 2. Pruebas manuales (checklist para antes de presentar)

Usuarios demo (`python manage.py seed_demo`; contraseña `Demo12345!`): `admin`, `recepcion`, `vet_ana`, `vet_luis`.

**Ejecución del 2026-11-03** (Claude Code controlando el navegador): los 20 casos se corrieron en **local** (Django, SQLite, datos demo) con usuarios `recepcion` y `vet_ana`; los datos de prueba se descartaron restaurando la base. En la URL de **Render** solo se verificó lo que no requiere sesión (login 200, HTTPS/HSTS, rutas protegidas redirigen, API sin sesión 403, login sin scroll horizontal a 375 px). **Falta repetir el recorrido con sesión en la URL de Render** (hacerlo a mano antes de presentar).

Observaciones: el caso 6 (búsqueda en vivo) reveló un error real: desde la segunda búsqueda la URL acumulaba `?q=a?q=ab…` y la tabla quedaba vacía; se corrigió en `static/js/app.js` y se volvió a probar. El caso 7 se verificó en la lista de citas (10 por página); las demás listas demo tienen menos de 10 registros. En el caso 10, la interfaz no ofrece las horas ocupadas, por lo que el traslape se probó contra `POST /api/citas/` (400 "El veterinario ya tiene una cita en ese horario").

| # | Caso | Pasos | Resultado esperado | ✔ |
|---|---|---|---|:-:|
| 1 | Login incorrecto | Usuario `admin`, clave mala | Mensaje "Usuario o contraseña incorrectos" | ✅ |
| 2 | Login correcto | `recepcion` / clave correcta | Entra al panel con menú de su rol | ✅ |
| 3 | Permisos veterinario | Entrar como `vet_ana` → ir a `/clientes/nuevo/` | Página "No tienes permiso" | ✅ |
| 4 | Permisos recepción | Como `recepcion` abrir `/expedientes/consultas/nueva/?mascota=1` | 403 | ✅ |
| 5 | Crear cliente | Recepción → Clientes → Nuevo, teléfono `123` | Error de teléfono; con `2222-3333` guarda | ✅ |
| 6 | Búsqueda en vivo | Clientes → escribir "lóp" | Tabla se filtra sin recargar la página | ✅ |
| 7 | Paginación | Lista con > 10 registros | Botones de página funcionan | ✅ |
| 8 | Crear mascota | Cliente → Agregar mascota, nacimiento futuro | Error; con fecha válida guarda | ✅ |
| 9 | Agendar cita | Citas → Agendar: elegir servicio, veterinario, fecha | La lista de horas se llena sola y no incluye las ocupadas | ✅ |
| 10 | Traslape | Agendar a la misma hora/veterinario (forzando) | Rechazo "ya tiene una cita" | ✅ |
| 11 | Domingo | Elegir un domingo | "Sin horarios libres ese día" | ✅ |
| 12 | Confirmar sin recargar | Lista de citas → botón ✔ | Toast verde y estado cambia a "Confirmada" | ✅ |
| 13 | Cancelar | Botón ✖ → aceptar confirmación | Estado "Cancelada"; se libera el horario | ✅ |
| 14 | Atender cita | `vet_ana` → cita confirmada → Atender → guardar | Consulta en expediente; cita "Atendida" | ✅ |
| 15 | Vacuna vencida | Mascota "Luna" | Marca "Vencida" en la vacuna | ✅ |
| 16 | Eliminar con relaciones | Eliminar cliente con mascotas | Mensaje "No se puede eliminar…" | ✅ |
| 17 | Panel | Abrir panel | Indicadores y 2 gráficas con datos | ✅ |
| 18 | Celular | Abrir en 375 px (F12 → móvil) | Menú ☰ deslizable, sin scroll horizontal | ✅ |
| 19 | API sin sesión | Abrir `/api/clientes/` en ventana privada | 403 | ✅ |
| 20 | Cerrar sesión | Menú de usuario → Cerrar sesión | Vuelve al login | ✅ |

## 3. Pruebas de seguridad realizadas

| Amenaza | Cómo se mitiga | Dónde verlo |
|---|---|---|
| Acceso sin sesión | `LoginRequiredMixin` / permisos DRF | `accounts/permissions.py` |
| Escalada de privilegios | Roles verificados **en el servidor** en cada vista y endpoint | `RolRequeridoMixin`, `RolPermiso` |
| CSRF | Middleware CSRF, `{% csrf_token %}`, cabecera `X-CSRFToken` en `fetch` | `static/js/app.js` |
| SQL Injection | Solo ORM de Django (consultas parametrizadas) | todas las vistas |
| XSS | Autoescape de plantillas; `textContent` en toasts | plantillas, `app.js` |
| Contraseñas débiles | Validadores de Django + hash PBKDF2 | `settings.py` |
| Clickjacking | `X-Frame-Options: DENY` | `settings.py` |
| Robo de sesión | Cookies `HttpOnly`/`Secure`, HTTPS + HSTS en producción | `settings.py` |
| Secretos en el repositorio | Variables de entorno, `.env` en `.gitignore` | `.env.example` |

Verificación de producción: `python manage.py check --deploy`.
