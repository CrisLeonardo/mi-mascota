# 9. Entrega y presentación

## 1. Estado de la entrega (2026-11-03)

Aplicación desplegada: **<https://mi-mascota-o2sm.onrender.com>** · Repositorio: <https://github.com/CrisLeonardo/mi-mascota> ·
Tablero: <https://github.com/users/CrisLeonardo/projects/1>

| # | Elemento | Estado |
|---|---|---|
| 1 | Negocio y levantamiento | Se usó el caso del enunciado (Veterinaria "Mi Mascota"). **No hubo entrevista a un negocio real**; `01_LEVANTAMIENTO_NEGOCIO.md` lo declara. |
| 2 | Integrantes y roles | Solo Cristopher Leonardo Zepeda Esquivel trabajó (todos los roles). Los otros 4 integrantes no participaron; está declarado en `02_PRD.md` y `04_SCRUM.md`. |
| 3 | Tablero | GitHub Projects con las 18 historias asignadas, cerradas con evidencia y en *Finalizado*. |
| 4 | Repositorio | GitHub, ramas `main` (protegida) y `develop`, PRs y CI en verde. Un solo autor de commits. |
| 5 | Despliegue | Render + PostgreSQL, HTTPS con HSTS. |
| 6 | Diagrama ER | `diagrama_er.html` y `diagrama_er.svg` (imagen exportada). |
| 7 | Estudio de la guía | `GUIA_DE_ESTUDIO.md`. |
| 8 | Pruebas manuales en la URL desplegada | Checklist de `06_PLAN_DE_PRUEBAS.md` (ejecutar en la URL real antes de presentar). |

## 2. Checklist final contra el enunciado

| Requisito del PDF | Cumplido con | ✔ |
|---|---|:-:|
| Negocio con problema, necesidad y solución | `01_LEVANTAMIENTO_NEGOCIO.md` (caso del enunciado, sin entrevista real) | ⚠️ |
| Equipo de 5 con Scrum y roles | `04_SCRUM.md`: un solo integrante participó | ⚠️ |
| PRD completo (nombre, descripción, problema, objetivo, alcance, fuera de alcance, usuarios, RF, RNF, criterios) | `02_PRD.md` | ✅ |
| Plataforma de gestión con las 5 columnas, responsables y evidencia | GitHub Projects | ✅ |
| Frontend profesional y responsivo (PC y móvil) | Bootstrap 5, plantillas Django | ✅ |
| Backend | Django | ✅ |
| Base de datos relacional + Diagrama ER | PostgreSQL, `03_DIAGRAMA_ER.md`, `diagrama_er.svg` | ✅ |
| Autenticación | Login/logout, cambio de contraseña | ✅ |
| Autorización (roles y permisos) | 3 roles, matriz de permisos | ✅ |
| CRUD | Clientes, mascotas, servicios, usuarios, citas, consultas, vacunas | ✅ |
| Validaciones cliente y servidor | HTML5 + Bootstrap + formularios y modelos Django | ✅ |
| AJAX / Fetch | Búsqueda en vivo, horarios libres, estados de cita, gráficas | ✅ |
| API REST | `/api/…` con DRF | ✅ |
| Búsquedas, filtros y paginación | Todos los listados | ✅ |
| Seguridad | CSRF, XSS, SQLi, hashing, HTTPS/HSTS | ✅ |
| Testing | 67 pruebas automáticas + checklist manual | ✅ |
| Git (commits, ramas, PRs, participación) | Repositorio con ramas y PRs; **un solo participante** | ⚠️ |
| CI/CD | GitHub Actions + despliegue automático en Render | ✅ |
| Aplicación desplegada | <https://mi-mascota-o2sm.onrender.com> | ✅ |

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
