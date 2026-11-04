# 🐾 Mi Mascota — Sistema de gestión veterinaria

Aplicación web para una clínica veterinaria: clientes, mascotas, agenda de citas sin traslapes, expedientes
clínicos, control de vacunas, panel de indicadores y API REST. Proyecto final del curso **Desarrollo Web**
(Universidad Mariano Gálvez de Guatemala).

**Aplicación desplegada:** <https://mi-mascota-o2sm.onrender.com> (plan gratuito de Render: la primera visita puede tardar ~30 s en despertar).

**Stack:** Django 5.2 · Django REST Framework · PostgreSQL (SQLite en local) · Bootstrap 5 · JavaScript (fetch) · Chart.js · GitHub Actions · Render

## Ejecutar en tu computadora

Requisitos: Python 3.12 o superior y Git.

```bash
# 1. Entorno virtual e instalación
python -m venv .venv
.venv\Scripts\activate            # Windows (PowerShell/CMD)
# source .venv/bin/activate       # macOS / Linux
pip install -r requirements.txt

# 2. Base de datos y datos de ejemplo
python manage.py migrate
python manage.py seed_demo

# 3. Servidor
python manage.py runserver
```

Abrir <http://localhost:8000>. Usuarios de demostración (contraseña `Demo12345!`):

| Usuario | Rol | Qué puede hacer |
|---|---|---|
| `admin` | Administrador | Todo, incluida la gestión de usuarios y servicios |
| `recepcion` | Recepcionista | Clientes, mascotas y citas |
| `vet_ana`, `vet_luis` | Veterinario | Su agenda, consultas y vacunas |

Variables opcionales en un archivo `.env` (ver `.env.example`): nombre y teléfono del negocio, horario, `DATABASE_URL`.

## Pruebas

```bash
python manage.py test        # 67 pruebas automáticas
```

## Estructura

```
config/        Configuración (settings, urls)
accounts/      Usuarios, roles y permisos
clientes/      Clientes y mascotas
servicios/     Catálogo de servicios
citas/         Agenda: reglas de negocio y horarios disponibles
expedientes/   Consultas y vacunas
api/           API REST (serializers, viewsets)
core/          Panel, utilidades compartidas, comandos (seed_demo, crear_admin)
templates/     Plantilla base y páginas de error
static/        CSS y JavaScript
docs/          Documentación del proyecto
```

## Documentación

| Documento | Contenido |
|---|---|
| [`docs/01_LEVANTAMIENTO_NEGOCIO.md`](docs/01_LEVANTAMIENTO_NEGOCIO.md) | Negocio, problema, necesidad, solución |
| [`docs/02_PRD.md`](docs/02_PRD.md) | Product Requirements Document |
| [`docs/03_DIAGRAMA_ER.md`](docs/03_DIAGRAMA_ER.md) | Diagrama Entidad-Relación y diccionario de datos |
| [`docs/04_SCRUM.md`](docs/04_SCRUM.md) | Roles, ceremonias, backlog y sprints |
| [`docs/05_GIT_Y_COLABORACION.md`](docs/05_GIT_Y_COLABORACION.md) | Ramas, Pull Requests, cómo repartir el trabajo |
| [`docs/06_PLAN_DE_PRUEBAS.md`](docs/06_PLAN_DE_PRUEBAS.md) | Pruebas automáticas, manuales y de seguridad |
| [`docs/07_DESPLIEGUE.md`](docs/07_DESPLIEGUE.md) | Publicar en Render con PostgreSQL |
| [`docs/08_API.md`](docs/08_API.md) | Endpoints de la API REST |
| [`docs/09_ENTREGA.md`](docs/09_ENTREGA.md) | Checklist contra la rúbrica y guion de presentación |

## Mapa contra la rúbrica del curso (15 pts)

| Criterio | Pts | Dónde está |
|---|:-:|---|
| Gestión y documentación | 3 | `docs/` · tablero Scrum · PRD · ER · repositorio con PRs |
| Calidad del código y dominio técnico | 4 | Apps separadas, reglas de negocio en el modelo, 67 pruebas |
| Funcionalidad y solución del problema | 5 | Agenda sin traslapes, expediente digital, vacunas, panel, roles |
| Tecnologías y arquitectura | 3 | Django + DRF + PostgreSQL + Bootstrap + fetch + CI/CD + despliegue |
