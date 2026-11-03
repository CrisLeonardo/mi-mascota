# 4. Gestión del proyecto con Scrum

> ⚠️ **Importante:** el enunciado dice que el tablero debe mostrar *"el historial real del trabajo realizado"* y que las
> tareas deben tener *responsables y evidencia*. Este documento es la **plantilla y el plan**; el tablero
> (Trello / GitHub Projects / Jira), las reuniones y el reparto de tareas **deben ser reales y hechos por el equipo**.
> Un tablero armado de golpe el último día se nota (las fechas de creación y movimiento quedan registradas).
> Los ✏️ son datos que ustedes completan.

## 1. Equipo y roles

| Integrante | Rol Scrum | Responsabilidad principal | Áreas técnicas que dominará |
|---|---|---|---|
| ✏️ Nombre 1 | **Product Owner** | Define y prioriza el Product Backlog; valida con el negocio | PRD, levantamiento, criterios de aceptación, pruebas de aceptación |
| ✏️ Nombre 2 | **Scrum Master** | Organiza reuniones, tablero, quita obstáculos | Git/GitHub (ramas, PR), CI/CD, despliegue |
| ✏️ Nombre 3 | Desarrollador | Backend | Modelos, vistas, reglas de negocio de citas |
| ✏️ Nombre 4 | Desarrollador | Frontend | Plantillas, Bootstrap, JavaScript/fetch |
| ✏️ Nombre 5 | Desarrollador | API y calidad | API REST, pruebas automáticas, seguridad |

Regla del curso: **todos deben saber explicar todo el proyecto** (ver `GUIA_DE_ESTUDIO.md`). El PO y el SM también
programan o documentan.

## 2. Herramienta de gestión

Tablero con estas columnas (mínimo exigido): **Product Backlog → Sprint Backlog → En progreso → Revisión/Testing → Finalizado**.

Cada tarjeta debe tener: responsable · historia de usuario · criterios de aceptación · etiqueta de sprint · y, al
pasar a *Finalizado*, **evidencia** (enlace al Pull Request, captura o GIF).

**Tablero del equipo:** <https://github.com/users/CrisLeonardo/projects/1> (GitHub Projects, ligado al repositorio). Las 18 historias están como issues (#1 a #18) con su hito de sprint, en la columna *Product Backlog* y sin responsable: cada integrante se asigna las suyas y las mueve con evidencia.

Para cargar el backlog de golpe (ya hecho en GitHub):
- **GitHub Projects:** crear issues con `docs/BACKLOG.csv` (o copiar a mano) usando la plantilla "Historia de usuario".
- **Trello:** *Importar CSV* con Power-Up "Import" o crear las tarjetas pegando la columna `Historia`.

## 3. Ceremonias

| Ceremonia | Frecuencia | Duración | Qué se hace | Evidencia |
|---|---|---|---|---|
| Sprint Planning | Inicio de cada sprint | 45 min | El PO presenta prioridades; el equipo elige historias y las divide en tareas | Captura del Sprint Backlog |
| Daily (breve) | 2-3 veces por semana (puede ser por chat) | 10 min | ¿Qué hice? ¿Qué haré? ¿Qué me bloquea? | Mensajes del grupo / acta corta |
| Sprint Review | Fin de sprint | 30 min | Demo de lo terminado al PO / docente | Captura o grabación |
| Retrospectiva | Fin de sprint | 20 min | Qué salió bien, qué mejorar, 1 acuerdo | Acta con acuerdos |

## 4. Plan de sprints

Sugerencia: sprints de **1 semana**. Ajusten la cantidad a las semanas que les queden.

| Sprint | Objetivo | Historias |
|---|---|---|
| **0 — Preparación** | Entender el negocio y dejar el entorno listo | Levantamiento, PRD, ER, repositorio, tablero, proyecto Django base, CI |
| **1 — Base y registros** | Acceso seguro y datos maestros | HU-01 a HU-06 (login, usuarios, roles, clientes, mascotas, servicios) |
| **2 — Agenda** | Citas sin traslapes | HU-07 a HU-10 |
| **3 — Clínica y panel** | Expediente, vacunas, indicadores, API | HU-11 a HU-15 |
| **4 — Calidad y entrega** | Pruebas, despliegue, documentación, ensayo de presentación | HU-16 a HU-18 |

## 5. Product Backlog (resumen)

Versión importable: [`BACKLOG.csv`](BACKLOG.csv). Puntos = esfuerzo relativo (1, 2, 3, 5, 8).

| ID | Historia de usuario | Prio | Pts | Sprint | RF |
|---|---|:-:|:-:|:-:|---|
| HU-01 | Como usuario quiero iniciar y cerrar sesión para proteger la información de la clínica. | Alta | 3 | 1 | RF-01 |
| HU-02 | Como administrador quiero crear y desactivar usuarios con un rol para controlar quién usa el sistema. | Alta | 5 | 1 | RF-02 |
| HU-03 | Como administrador quiero que cada rol vea solo lo que le corresponde para evitar cambios indebidos. | Alta | 5 | 1 | RF-03 |
| HU-04 | Como recepcionista quiero registrar y buscar clientes para atender más rápido. | Alta | 5 | 1 | RF-04, RF-06 |
| HU-05 | Como recepcionista quiero registrar las mascotas de un cliente para armar su ficha. | Alta | 5 | 1 | RF-05 |
| HU-06 | Como administrador quiero gestionar los servicios y precios para mantener el catálogo al día. | Media | 3 | 1 | RF-07 |
| HU-07 | Como recepcionista quiero agendar una cita viendo solo horas libres para no duplicar horarios. | Alta | 8 | 2 | RF-08, RF-09 |
| HU-08 | Como recepcionista quiero editar una cita para reprogramarla. | Media | 3 | 2 | RF-08 |
| HU-09 | Como recepcionista quiero confirmar, cancelar o marcar "no asistió" sin recargar la página para trabajar ágil. | Media | 5 | 2 | RF-10, RF-11 |
| HU-10 | Como veterinario quiero ver mis citas del día para organizar mi jornada. | Alta | 3 | 2 | RF-16 |
| HU-11 | Como veterinario quiero registrar la consulta de una cita para dejarla en el expediente. | Alta | 8 | 3 | RF-12 |
| HU-12 | Como veterinario quiero registrar una consulta sin cita para atender urgencias. | Media | 2 | 3 | RF-13 |
| HU-13 | Como veterinario quiero ver el historial completo de una mascota para decidir el tratamiento. | Alta | 5 | 3 | RF-14 |
| HU-14 | Como veterinario quiero registrar vacunas y su próximo refuerzo para dar seguimiento. | Alta | 5 | 3 | RF-15 |
| HU-15 | Como administrador quiero un panel con indicadores y gráficas para tomar decisiones. | Media | 5 | 3 | RF-16, RF-17 |
| HU-16 | Como equipo queremos pruebas automáticas e integración continua para detectar errores a tiempo. | Alta | 5 | 4 | RNF-07 |
| HU-17 | Como cliente del proyecto quiero la aplicación en Internet para usarla desde cualquier lugar. | Alta | 5 | 4 | RNF-08 |
| HU-18 | Como equipo queremos documentación y guion de presentación para exponer el proyecto. | Alta | 3 | 4 | — |

**Total:** 18 historias · 83 puntos.

## 6. Reparto sugerido (para evitar que una persona haga todo)

Cada integrante debe tener **commits y Pull Requests propios** en todos los sprints. Una forma equilibrada:

| Integrante | Sprint 1 | Sprint 2 | Sprint 3 | Sprint 4 |
|---|---|---|---|---|
| 1 (PO) | HU-04 (UI clientes), PRD | HU-10 | HU-13 (historial) | HU-18 |
| 2 (SM) | HU-01, repo + CI | HU-08 | HU-12 | HU-17 (despliegue) |
| 3 (Back) | HU-02, HU-03 | HU-07 (reglas de citas) | HU-11 | HU-16 (pruebas citas) |
| 4 (Front) | HU-05, HU-06 | HU-09 (fetch estados) | HU-14 | HU-16 (pruebas UI) |
| 5 (API) | HU-04 (búsqueda) | API de citas | HU-15 (panel + API) | HU-16 (pruebas API) |

> El código ya está construido. Para que el historial de Git/tablero sea honesto, repártanse **módulos para
> estudiar, mejorar y extender** (por ejemplo: cada uno agrega pruebas, mejora la UI de su módulo, corrige
> detalles o amplía una funcionalidad con su propio Pull Request). Vean `05_GIT_Y_COLABORACION.md`.

## 7. Seguimiento (burndown simple)

Lleven esta tabla actualizada al cierre de cada sprint ✏️:

| Sprint | Puntos planeados | Puntos terminados | Observaciones / lecciones |
|---|:-:|:-:|---|
| 0 | — | — | |
| 1 | 26 | | |
| 2 | 19 | | |
| 3 | 25 | | |
| 4 | 13 | | |

## 8. Plantilla de acta de retrospectiva ✏️

```
Sprint N — Fecha:
Asistentes:
✅ Qué salió bien:
⚠️ Qué mejorar:
🎯 Acuerdo para el próximo sprint:
```
