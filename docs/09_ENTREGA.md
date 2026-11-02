# 9. Entrega y presentación

## 1. Qué ya está hecho y qué deben hacer ustedes

El código, la base de datos, la API, las pruebas, el CI y la documentación técnica **ya están construidos**.
Lo que el enunciado evalúa y que **solo el equipo puede hacer de forma real** es:

| # | Pendiente del equipo | Dónde | Pts de rúbrica |
|---|---|---|:-:|
| 1 | Elegir/confirmar el negocio **real**, hacer la visita o entrevista y completar los ✏️ | `01_LEVANTAMIENTO_NEGOCIO.md` | Gestión (3) |
| 2 | Escribir nombres e integrantes y roles Scrum | `02_PRD.md`, `04_SCRUM.md` | Gestión (3) |
| 3 | Crear el tablero (Trello/GitHub Projects), cargar `BACKLOG.csv`, asignar responsables y mover tarjetas con evidencia | `04_SCRUM.md` | Gestión (3) |
| 4 | Crear el repositorio en GitHub, que **cada integrante** haga sus commits y Pull Requests | `05_GIT_Y_COLABORACION.md` | Gestión (3) / Código (4) |
| 5 | Desplegar en Render y probar la URL | `07_DESPLIEGUE.md` | Tecnología (3) |
| 6 | Exportar el diagrama ER a imagen y ponerlo en la presentación | `diagrama_er.html` | Gestión (3) |
| 7 | **Estudiar la guía** y ensayar la presentación | `GUIA_DE_ESTUDIO.md` | Código/dominio (4) |
| 8 | Hacer el checklist de pruebas manuales en la URL desplegada | `06_PLAN_DE_PRUEBAS.md` | Funcionalidad (5) |

## 2. Checklist final contra el enunciado

| Requisito del PDF | Cumplido con | ✔ |
|---|---|:-:|
| Negocio real con problema, necesidad y solución | `01_LEVANTAMIENTO_NEGOCIO.md` (completar con datos reales) | ☐ |
| Equipo de 5 con Scrum y roles | `04_SCRUM.md` + tablero | ☐ |
| PRD completo (nombre, descripción, problema, objetivo, alcance, fuera de alcance, usuarios, RF, RNF, criterios) | `02_PRD.md` | ✅ |
| Plataforma de gestión con las 5 columnas, responsables y evidencia | Tablero del equipo | ☐ |
| Frontend profesional y responsivo (PC y móvil) | Bootstrap 5, plantillas Django | ✅ |
| Backend | Django | ✅ |
| Base de datos relacional + Diagrama ER | PostgreSQL, `03_DIAGRAMA_ER.md` | ✅ |
| Autenticación | Login/logout, cambio de contraseña | ✅ |
| Autorización (roles y permisos) | 3 roles, matriz de permisos | ✅ |
| CRUD | Clientes, mascotas, servicios, usuarios, citas, consultas, vacunas | ✅ |
| Validaciones cliente y servidor | HTML5 + Bootstrap + formularios y modelos Django | ✅ |
| AJAX / Fetch | Búsqueda en vivo, horarios libres, estados de cita, gráficas | ✅ |
| API REST | `/api/…` con DRF | ✅ |
| Búsquedas, filtros y paginación | Todos los listados | ✅ |
| Seguridad | CSRF, XSS, SQLi, hashing, HTTPS/HSTS | ✅ |
| Testing | 67 pruebas automáticas + checklist manual | ✅ |
| Git (commits, ramas, PRs, participación) | Repositorio del equipo | ☐ |
| CI/CD | GitHub Actions + despliegue automático en Render | ✅ (al subir a GitHub) |
| Aplicación desplegada | Render | ☐ |

## 3. Guion de presentación (15 minutos, 5 personas)

Cada persona habla ~3 minutos y **contesta preguntas de cualquier parte**.

| Min | Quién sugerido | Contenido |
|---|---|---|
| 0-3 | Product Owner | Negocio, problema real, necesidad, solución. Mostrar el PRD (alcance / fuera de alcance) y las historias priorizadas. |
| 3-5 | Scrum Master | Cómo trabajaron: roles, sprints, tablero con evidencia, GitHub (ramas, PRs, contribuidores), CI en verde. |
| 5-10 | Todos (demo en vivo) | Ver guion de demo abajo. |
| 10-13 | Desarrolladores | Arquitectura (apps, MVT), diagrama ER, reglas de negocio de citas, API REST, seguridad, pruebas. |
| 13-15 | Todos | Despliegue, limitaciones/trabajo futuro, preguntas. |

### Guion de la demo (5 min)

1. **Login como `recepcion`** → mostrar el panel (indicadores y gráficas, que vienen de la API).
2. **Clientes** → escribir en el buscador (se filtra sin recargar) → abrir un cliente → *Agregar mascota*.
3. **Agendar cita** → elegir servicio, veterinario, fecha → *aparecen solo las horas libres* → guardar.
   Intentar la misma hora otra vez desde otra mascota → muestra que **no deja duplicar**.
4. **Lista de citas** → *Confirmar* con un clic (aviso verde, sin recargar).
5. Intentar entrar a `/cuentas/usuarios/` → **403** (permisos por rol).
6. **Cerrar sesión, entrar como `vet_ana`** → panel con *solo sus citas* → *Atender* → llenar consulta → guardar
   → la cita pasa a *Atendida* y la consulta aparece en el expediente de la mascota.
7. Registrar una **vacuna** con refuerzo próximo → verlo en el panel de refuerzos.
8. Mostrar la app en un celular (o modo responsivo del navegador).
9. (Opcional) Mostrar `/api/` y las pruebas en verde en GitHub Actions.

### Plan B si falla el internet o el hosting
- Tener el proyecto corriendo en local (`python manage.py runserver`) con `seed_demo`.
- Tener un video corto de la demo grabado.
- Abrir la URL de Render 5 minutos antes (plan gratuito se duerme).

## 4. Preguntas que suele hacer el docente

Las respuestas están desarrolladas en la sección 17 de `GUIA_DE_ESTUDIO.md`.
