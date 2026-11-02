# 2. PRD — Product Requirements Document

| | |
|---|---|
| **Producto** | Mi Mascota — Sistema de gestión para clínica veterinaria |
| **Versión** | 1.0 |
| **Equipo** | ✏️ Nombres de los 5 integrantes y su rol (ver `04_SCRUM.md`) |
| **Curso** | Desarrollo Web — Universidad Mariano Gálvez de Guatemala |

## 1. Nombre del proyecto

**Mi Mascota — Sistema web de gestión veterinaria.**

## 2. Descripción del negocio

Veterinaria de barrio que ofrece consulta general, vacunación, desparasitación, estética y cirugías menores.
Atiende de lunes a sábado de 8:00 a 17:00 con dos veterinarios, una recepcionista y un administrador.
Detalle completo en `01_LEVANTAMIENTO_NEGOCIO.md`.

## 3. Problema

Las citas se anotan en una agenda de papel y por teléfono, lo que produce citas duplicadas; los expedientes
clínicos están en fichas físicas difíciles de consultar, no hay control de refuerzos de vacunas ni
información sobre el desempeño del negocio.

## 4. Objetivo

**General:** digitalizar la operación diaria de la clínica con una aplicación web segura y fácil de usar.

**Específicos**
1. Registrar clientes y mascotas en una base de datos relacional.
2. Agendar citas sin traslapes de horario.
3. Mantener el expediente clínico (consultas y vacunas) de cada mascota.
4. Controlar los refuerzos de vacunas próximos.
5. Mostrar indicadores del negocio en un panel.
6. Restringir las acciones según el rol del usuario.

## 5. Alcance (qué hará el sistema)

- Inicio y cierre de sesión; cambio de contraseña.
- Administración de usuarios y roles (solo administrador).
- CRUD de clientes, mascotas y servicios, con búsqueda, filtros y paginación.
- Agenda de citas con horarios disponibles calculados, estados y cambio de estado sin recargar la página.
- Registro de consultas (síntomas, diagnóstico, tratamiento, peso, temperatura, costo) vinculadas o no a una cita.
- Registro de vacunas con fecha de refuerzo y alertas de vencimiento.
- Panel con indicadores y gráficas.
- API REST documentada con autenticación por sesión y por token.
- Interfaz responsiva (computadora y celular).

## 6. Fuera de alcance (qué NO hará)

- Facturación electrónica (FEL/SAT) ni cobro en línea.
- Inventario de medicamentos y control de compras a proveedores.
- Portal público para que el cliente agende por sí mismo.
- Envío automático de mensajes por WhatsApp/SMS/correo (solo se listan los refuerzos para llamar).
- Aplicación móvil nativa (la web es responsiva).
- Contabilidad ni planillas.
- Múltiples sucursales.

## 7. Usuarios

| Rol | Descripción | Qué necesita |
|---|---|---|
| **Administrador** | Dueño o gerente | Control total, usuarios, servicios, indicadores |
| **Recepcionista** | Atiende teléfono y mostrador | Registrar clientes/mascotas y agendar citas |
| **Veterinario** | Atiende pacientes | Ver su agenda, registrar consultas y vacunas, consultar el historial |

### Matriz de permisos

| Módulo | Administrador | Recepcionista | Veterinario |
|---|:-:|:-:|:-:|
| Usuarios | Crear / editar / activar | — | — |
| Clientes y mascotas | CRUD | CRUD | Solo lectura |
| Servicios | CRUD | Solo lectura | Solo lectura |
| Citas | CRUD + estado | CRUD + estado | Solo lectura + estado |
| Consultas y vacunas | CRUD | Solo lectura | CRUD |
| Panel | Sí | Sí | Sí (sus citas) |

## 8. Requerimientos funcionales

| ID | Requerimiento | Prioridad |
|---|---|:-:|
| RF-01 | El sistema permitirá iniciar y cerrar sesión con usuario y contraseña. | Alta |
| RF-02 | El administrador podrá crear, editar y activar/desactivar usuarios con un rol. | Alta |
| RF-03 | El sistema aplicará permisos según el rol en cada pantalla y en la API. | Alta |
| RF-04 | Se podrán registrar, consultar, editar y eliminar clientes. | Alta |
| RF-05 | Se podrán registrar, consultar, editar y eliminar mascotas asociadas a un cliente. | Alta |
| RF-06 | Los listados tendrán búsqueda, filtros y paginación; la búsqueda se actualizará sin recargar la página. | Media |
| RF-07 | El administrador gestionará el catálogo de servicios (precio y duración). | Alta |
| RF-08 | Se podrán agendar citas eligiendo mascota, servicio, veterinario, fecha y hora. | Alta |
| RF-09 | El sistema mostrará solo las horas libres del veterinario y rechazará traslapes, domingos, horas pasadas y fuera de horario. | Alta |
| RF-10 | Las citas tendrán estados (pendiente, confirmada, atendida, cancelada, no asistió) con transiciones controladas. | Alta |
| RF-11 | El estado de una cita se podrá cambiar desde la lista sin recargar la página. | Media |
| RF-12 | Se podrá registrar la consulta de una cita, que pasará automáticamente a "atendida". | Alta |
| RF-13 | Se podrá registrar una consulta sin cita previa (urgencia). | Media |
| RF-14 | Cada mascota tendrá un expediente con su historial de consultas, vacunas y citas. | Alta |
| RF-15 | Se podrán registrar vacunas con fecha de próxima dosis y ver las vencidas o próximas a vencer. | Alta |
| RF-16 | El panel mostrará citas del día, indicadores, ingresos de 30 días y gráficas. | Media |
| RF-17 | El sistema expondrá una API REST (clientes, mascotas, servicios, citas, horarios, estadísticas). | Media |
| RF-18 | No se podrán eliminar registros con historial asociado; se ofrecerá desactivarlos. | Media |

## 9. Requerimientos no funcionales

| ID | Categoría | Requerimiento |
|---|---|---|
| RNF-01 | Seguridad | Contraseñas almacenadas con hash (PBKDF2); validadores de contraseña; sesión de 8 horas; cookies `HttpOnly`. |
| RNF-02 | Seguridad | Protección CSRF en todos los formularios y peticiones `fetch`; ORM con consultas parametrizadas (sin SQL injection); autoescape de plantillas (sin XSS). |
| RNF-03 | Seguridad | En producción: HTTPS forzado, HSTS, cookies `Secure`, `X-Frame-Options: DENY`; secretos solo en variables de entorno. |
| RNF-04 | Seguridad | Autorización en el servidor por rol (no basta con ocultar botones). |
| RNF-05 | Usabilidad | Interfaz responsiva (≥ 360 px de ancho), validación en el cliente con mensajes claros en español. |
| RNF-06 | Rendimiento | Listados paginados (10 por página), consultas con `select_related` e índices en las columnas de búsqueda y de agenda. |
| RNF-07 | Mantenibilidad | Código organizado por apps de Django, ≥ 50 pruebas automáticas, integración continua en GitHub Actions. |
| RNF-08 | Disponibilidad | Aplicación desplegada en Internet con base de datos PostgreSQL administrada. |
| RNF-09 | Compatibilidad | Chrome, Edge, Firefox y Safari actuales. |
| RNF-10 | Integridad | Reglas de negocio validadas en el servidor (modelo) y claves foráneas `PROTECT` para conservar el historial. |

## 10. Criterios de aceptación (por funcionalidad)

| Req. | Criterio de aceptación (Dado / Cuando / Entonces) |
|---|---|
| RF-01 | **Dado** un usuario activo, **cuando** ingresa credenciales correctas, **entonces** entra al panel; con credenciales incorrectas ve un mensaje y no entra. Un usuario desactivado no puede entrar. |
| RF-03 | **Dado** un veterinario, **cuando** intenta abrir `/clientes/nuevo/` o `/cuentas/usuarios/`, **entonces** recibe la página "No tienes permiso" (403). |
| RF-05 | **Dado** un cliente existente, **cuando** la recepción registra una mascota con fecha de nacimiento futura, **entonces** el sistema la rechaza con un mensaje. |
| RF-06 | **Dado** 25 clientes, **cuando** se abre la lista, **entonces** se muestran 10 por página; al escribir en el buscador la tabla se filtra sin recargar. |
| RF-09 | **Dado** un veterinario con cita a las 10:00 (30 min), **cuando** se agenda otra a las 10:15 con él, **entonces** se rechaza; a las 10:30 se acepta. El selector de horas no ofrece 10:00 ni 10:30 si están ocupadas. |
| RF-10 | **Dado** una cita cancelada, **cuando** se intenta confirmar, **entonces** el sistema responde error 400 y el estado no cambia. |
| RF-12 | **Dado** una cita confirmada, **cuando** el veterinario guarda la consulta, **entonces** la consulta queda en el expediente y la cita pasa a "atendida". Una cita cancelada no se puede atender. |
| RF-15 | **Dado** una vacuna con próxima dosis anterior a hoy, **cuando** se consulta, **entonces** aparece marcada como "Vencida". |
| RF-17 | **Dado** un token válido, **cuando** se consulta `GET /api/clientes/`, **entonces** responde 200 con resultados paginados; sin credenciales responde 403. |
| RF-18 | **Dado** un cliente con mascotas, **cuando** se intenta eliminar, **entonces** no se elimina y se informa que debe desactivarlo. |

## 11. Definición de Terminado (DoD)

Una historia está terminada cuando: cumple sus criterios de aceptación · tiene validaciones en cliente y servidor ·
respeta permisos por rol · tiene pruebas automáticas que pasan · se ve bien en celular · fue revisada por otro
integrante mediante Pull Request · está integrada en `main` y la tarjeta pasó a "Finalizado" con evidencia.

## 12. Riesgos

| Riesgo | Probabilidad | Mitigación |
|---|:-:|---|
| Un integrante hace casi todo el trabajo | Media | Tablero con responsables, Pull Requests obligatorios con revisor distinto, revisión semanal de commits. |
| Choques de código en Git | Media | Ramas por funcionalidad, `main` protegida, integración frecuente. |
| Falla el despliegue el día de la presentación | Baja | Desplegar desde el Sprint 2, `render.yaml` versionado, datos demo reproducibles. |
| Plan gratuito del hosting "duerme" la app | Alta | Abrir la URL 5 minutos antes de presentar; tener video de respaldo. |

## 13. Stack tecnológico y justificación

| Capa | Tecnología | Por qué |
|---|---|---|
| Backend | Django 5.2 (Python) | Autenticación, ORM, formularios y seguridad integrados; permitido por el enunciado. |
| API | Django REST Framework | Estándar para APIs REST en Django. |
| Base de datos | PostgreSQL (producción) / SQLite (desarrollo) | Relacional; Postgres es robusto y gratuito en Render. |
| Frontend | Plantillas Django + Bootstrap 5 + JavaScript (fetch) | Interfaz responsiva sin complejidad extra; Bootstrap está en el enunciado. |
| Gráficas | Chart.js | Ligera, sin dependencias. |
| Pruebas | `django.test` | Incluido en el framework. |
| CI/CD | GitHub Actions + Render | Pruebas automáticas y despliegue desde GitHub. |
