# Mi Mascota — contexto para continuar el trabajo

Sistema web de gestión para una **veterinaria** (negocio por defecto = ejemplo del PDF del curso; el equipo aún no
confirmó un negocio real). Proyecto final de Desarrollo Web, Universidad Mariano Gálvez. Equipo de 5 con Scrum.

## Estado (2026-11-02)

**Hecho y verificado:** código completo, 67 pruebas pasando en SQLite (1 se omite: solo corre en PostgreSQL) y
**67/67 en PostgreSQL 16 + Python 3.12 + `DEBUG=False`** (pasos del CI reproducidos en Docker el 2026-11-02),
`check --deploy` limpio, interfaz probada en navegador (login, horarios por fetch, cambio de estado, gráficas,
sin scroll horizontal en 375 px). Documentación y guía de estudio escritas.

**No hecho / no verificado:**
- Repo creado: **https://github.com/CrisLeonardo/mi-mascota** (público), ramas `main` y `develop`, commit inicial de
  Cristopher. CI en verde en ambas (67 pruebas en PostgreSQL). `main` protegida: PR con 1 aprobación, check
  `pruebas` obligatorio y al día, conversaciones resueltas, sin force push ni borrado (`enforce_admins` desactivado:
  el dueño puede saltarse la regla en emergencias). `develop` sin protección. **Falta:** invitar a los otros 4
  integrantes (Settings → Collaborators).
  **No commitear a nombre del equipo**: cada integrante debe tener commits propios (ver `docs/05_GIT_Y_COLABORACION.md`).
- Tablero Scrum creado: https://github.com/users/CrisLeonardo/projects/1 (privado, ligado al repo; 5 columnas del enunciado). 18 historias = issues #1-#18 con hitos Sprint 1-4, **sin responsable ni cerradas a propósito** (el equipo las toma y mueve con evidencia; no marcar nada como Finalizado por ellos). Falta: darle acceso al proyecto a los compañeros y decidir si se hace público para el docente.
- No desplegado en Render.
- Tablero Scrum, entrevista al negocio real, nombres de integrantes (marcados con ✏️ en `docs/`) los debe completar el equipo. No fabricar historial ni evidencia.
- Screenshots del navegador fallaron en la sesión; el responsivo se verificó con mediciones, no a ojo.

## Stack y comandos (Windows, Python 3.14 local; CI/Render usan 3.12)

PC actual: Python 3.14 está en `%LOCALAPPDATA%\Programs\Python\Python314` (no está en PATH; `python` en PATH es 3.11
de la Store). El venv se recreó con esa 3.14. Si se copia el proyecto a otra PC, **borrar y recrear `.venv`**
(guarda rutas absolutas). Docker Desktop instalado: PostgreSQL de prueba = contenedor `mascota-pg` (red `mascota-net`,
puerto 5433, usuario/clave `postgres`); `docker start mascota-pg` para reutilizarlo.

Django 5.2 + DRF, Bootstrap 5 (CDN), JS con fetch, Chart.js, PostgreSQL (`DATABASE_URL`) / SQLite, WhiteNoise + Gunicorn.

```bash
.venv\Scripts\activate           # el venv ya existe en mi-mascota/.venv
python manage.py runserver
python manage.py test            # 67 pruebas
python manage.py seed_demo       # usuarios admin/recepcion/vet_ana/vet_luis, clave Demo12345!
python manage.py makemigrations --check --dry-run
```
`db.sqlite3` actual = base limpia con datos demo (ignorada por git).

## Arquitectura (patrón repetido en cada app: models / forms / views / urls / templates / tests)

`accounts` (Usuario con campo `rol`, `permissions.py`) · `clientes` (Cliente, Mascota) · `servicios` · `citas` ·
`expedientes` (Consulta, Vacuna) · `api` (DRF) · `core` (panel, mixins, validadores, comandos `seed_demo`/`crear_admin`).

Decisiones que no hay que deshacer sin motivo:
- **Autorización en el servidor**: `RolRequeridoMixin` (vistas) y `RolPermiso` (API). Los botones ocultos (`puede_gestionar`, `puede_atender`) son solo comodidad.
- **Reglas de agenda en `Cita.clean()`** (traslapes de veterinario y mascota, horario, domingos). Formulario y API reutilizan esa misma lógica. `horarios_disponibles()` en `citas/models.py`.
- **Condición de carrera resuelta en `Cita.save()`**: con estado activo y sin `update_fields`, bloquea veterinario y mascota con `select_for_update()` (en ese orden) dentro de `transaction.atomic()` y re-revisa traslapes → `ValidationError`. `GuardarCitaMixin` (vistas) y `CitaViewSet._guardar` (API, 400) lo convierten en error normal. `CitaConcurrenciaTests` (hilos) solo corre en PostgreSQL. Guía §9.6.
- `Cita.duracion_minutos` se copia del servicio al guardar (desnormalización intencional).
- Estado "Atendida" solo se asigna al guardar la consulta (`@transaction.atomic`); `Cita.TRANSICIONES` controla el resto. Las citas no se borran por la API.
- `on_delete=PROTECT` en relaciones clínicas; borrado protegido (`EliminarProtegidoView`, API responde 409). Usuarios se desactivan, no se borran.
- Búsqueda en vivo: `ParcialListMixin` devuelve el fragmento `_*_tabla.html` con `?parcial=1`; `static/js/app.js` hace el fetch.
- `CitaForm` arma `fecha_hora` desde `fecha`+`hora` y reubica errores con `_update_errors`.
- WhiteNoise solo se agrega al middleware si `DEBUG=False`; con `DEBUG=False` las plantillas necesitan `collectstatic` antes de correr pruebas (por eso el CI lo ejecuta primero).
- `SECRET_KEY` es obligatoria cuando `DJANGO_DEBUG=False`.

## Limitaciones conocidas (documentadas en `GUIA_DE_ESTUDIO.md` §19)

Agenda protegida solo desde Django (sin `ExclusionConstraint`), sin bloqueo de login por intentos, sin recordatorios automáticos,
sin auditoría, sin pruebas automatizadas de UI.

## Documentación

`GUIA_DE_ESTUDIO.md` (guía didáctica para el equipo, con preguntas del docente y ejercicios) · `README.md` · `docs/01..09`
(levantamiento, PRD, ER + `diagrama_er.html`, Scrum + `BACKLOG.csv`, Git, pruebas, despliegue en Render, API, entrega/presentación).
Si cambias código o comportamiento, actualiza la guía, el PRD/API y la cifra de pruebas (aparece en README, guía, `docs/06`, `docs/09`).

## Siguientes pasos probables

1. Que el equipo confirme el negocio real y complete los ✏️.
2. Invitar colaboradores (ver arriba); cada integrante trabaja en ramas desde `develop` con PRs.
3. Desplegar en Render (`render.yaml`, `build.sh`), probar con el checklist de `docs/06`.
4. Ejercicios 1-3 de la guía como contribuciones individuales con sus propios PRs.
5. Opcional: `django-axes` (bloqueo de login); `ExclusionConstraint` como defensa extra a nivel de base.
