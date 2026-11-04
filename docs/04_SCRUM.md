# 4. Gestión del proyecto con Scrum

> **Transparencia:** el grupo está inscrito con 5 integrantes, pero **solo Cristopher Leonardo Zepeda Esquivel
> trabajó en el proyecto**; los demás no respondieron ni participaron. Por eso este documento no inventa
> reuniones, retrospectivas ni repartos de tareas que no ocurrieron: el tablero y el historial de Git reflejan que
> una sola persona asumió todos los roles.

## 1. Equipo y roles

| Integrante | Rol Scrum | Responsabilidad principal | Áreas técnicas |
|---|---|---|---|
| Cristopher Leonardo Zepeda Esquivel (`CrisLeonardo`) | **Product Owner, Scrum Master y Desarrollador** (todos los roles) | Priorizar el backlog, organizar el tablero y construir, probar y desplegar el sistema | PRD y levantamiento, Git/GitHub y CI, backend, frontend, API REST, pruebas, seguridad y despliegue |
| Otros 4 integrantes del grupo | Sin participación | — | — |

Regla del curso: **todos deben saber explicar todo el proyecto** (ver `GUIA_DE_ESTUDIO.md`). El PO y el SM también
programan o documentan.

## 2. Herramienta de gestión

Tablero con estas columnas (mínimo exigido): **Product Backlog → Sprint Backlog → En progreso → Revisión/Testing → Finalizado**.

Cada tarjeta debe tener: responsable · historia de usuario · criterios de aceptación · etiqueta de sprint · y, al
pasar a *Finalizado*, **evidencia** (enlace al Pull Request, captura o GIF).

**Tablero del equipo:** <https://github.com/users/CrisLeonardo/projects/1> (GitHub Projects, ligado al repositorio). Las 18 historias son los issues #1 a #18 con su hito de sprint, asignadas a `CrisLeonardo`. Cada una se cerró con un comentario de evidencia (commits, PR, ejecución de CI y URL desplegada) y está en la columna *Finalizado*. El tablero y los issues conservan las fechas reales de creación y cierre.

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

## 6. Reparto del trabajo

Las 18 historias (83 puntos) fueron desarrolladas por Cristopher Leonardo Zepeda Esquivel. El reparto sugerido en
la plantilla original (un integrante por módulo) **no se pudo aplicar** porque el resto del grupo no participó.
Se deja constancia en lugar de simular contribuciones: el historial de commits y Pull Requests del repositorio
muestra un único autor.

## 7. Seguimiento

| Sprint | Puntos planeados | Puntos terminados | Observaciones |
|---|:-:|:-:|---|
| 0 | — | — | Levantamiento, PRD, ER, repositorio, tablero y proyecto base (un solo integrante). |
| 1 | 26 | 26 | HU-01 a HU-06. |
| 2 | 19 | 19 | HU-07 a HU-10. |
| 3 | 25 | 25 | HU-11 a HU-15. |
| 4 | 13 | 13 | HU-16 a HU-18: 67 pruebas, CI en GitHub Actions, despliegue en Render y documentación. |

Los sprints son una **agrupación lógica de las historias**; no hubo reuniones de planificación, daily ni
retrospectivas con un equipo, porque el trabajo lo realizó una sola persona.

## 8. Lecciones aprendidas

- ⚠️ **Principal riesgo materializado:** el grupo de 5 quedó en 1 persona. Se mitigó automatizando lo repetible
  (pruebas y CI) y documentando todo para que cualquier integrante pudiera retomar el proyecto.
- ✅ Funcionó: ramas `develop`/`main` con `main` protegida, CI obligatorio y despliegue continuo desde `main`.
- 🎯 Para otro proyecto: confirmar la participación real del equipo en la primera semana y repartir módulos desde el inicio.
