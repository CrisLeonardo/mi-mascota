# 📘 Guía de estudio — Mi Mascota

> Esta guía está escrita para personas que **no conocen el proyecto**. Léanla en orden: va de lo general
> (qué es y para qué sirve) a lo técnico (cómo funciona cada pieza) y termina con las preguntas que puede hacer
> el docente y ejercicios para practicar. El enunciado exige que **todos los integrantes puedan explicar el
> proyecto completo**, no solo "su parte".

---

## Índice

0. [Ruta de estudio sugerida](#0-ruta-de-estudio-sugerida)
1. [El proyecto en 2 minutos](#1-el-proyecto-en-2-minutos)
2. [Conceptos que necesitas dominar](#2-conceptos-que-necesitas-dominar)
3. [Tecnologías usadas y por qué](#3-tecnologías-usadas-y-por-qué)
4. [Mapa de carpetas y archivos](#4-mapa-de-carpetas-y-archivos)
5. [Qué pasa cuando haces clic: el viaje de una petición](#5-qué-pasa-cuando-haces-clic-el-viaje-de-una-petición)
6. [Base de datos y modelos](#6-base-de-datos-y-modelos)
7. [Autenticación y autorización (roles)](#7-autenticación-y-autorización-roles)
8. [Formularios y validaciones](#8-formularios-y-validaciones)
9. [La parte estrella: reglas de la agenda de citas](#9-la-parte-estrella-reglas-de-la-agenda-de-citas)
10. [Vistas y mixins](#10-vistas-y-mixins)
11. [Plantillas y herencia](#11-plantillas-y-herencia)
12. [Frontend: Bootstrap y JavaScript (fetch)](#12-frontend-bootstrap-y-javascript-fetch)
13. [La API REST](#13-la-api-rest)
14. [Seguridad](#14-seguridad)
15. [Pruebas automáticas](#15-pruebas-automáticas)
16. [Git, CI/CD y despliegue](#16-git-cicd-y-despliegue)
17. [Preguntas del docente (con respuestas)](#17-preguntas-del-docente-con-respuestas)
18. [Ejercicios prácticos](#18-ejercicios-prácticos)
19. [Limitaciones y mejoras futuras (sé honesto con esto)](#19-limitaciones-y-mejoras-futuras)
20. [Glosario](#20-glosario)
21. [Autoevaluación](#21-autoevaluación)

---

## 0. Ruta de estudio sugerida

| Día | Qué hacer | Tiempo |
|---|---|---|
| 1 | Leer secciones **1 a 4**. Instalar y **correr el proyecto** (README). Entrar con los 3 roles y recorrer todas las pantallas. | 2-3 h |
| 2 | Secciones **5 y 6**. Abrir `models.py` de cada app y el diagrama ER. Mirar la base con el admin de Django (`/admin/`). | 2 h |
| 3 | Secciones **7 a 11**. Seguir con el editor el flujo de "agendar cita" archivo por archivo. | 3 h |
| 4 | Secciones **12 a 16**. Usar F12 (pestaña *Network*) mientras usas la app para **ver los `fetch`** en vivo. Correr las pruebas. | 3 h |
| 5 | Secciones **17 a 21**. Hacer los ejercicios 1-3. Ensayar la presentación (`docs/09_ENTREGA.md`). | 3 h |

**Reparto para profundizar** (cada uno se vuelve "experto" en un tema, pero todos conocen todo):

| Persona | Tema profundo | Secciones |
|---|---|---|
| 1 (PO) | Negocio, PRD, criterios de aceptación, demo | 1, 17 + `docs/01`, `02` |
| 2 (SM) | Git, CI/CD, despliegue, Scrum | 16 + `docs/04`, `05`, `07` |
| 3 | Modelos, reglas de citas, base de datos | 6, 9 |
| 4 | Plantillas, Bootstrap, JavaScript | 11, 12 |
| 5 | API REST, seguridad, pruebas | 13, 14, 15 |

---

## 1. El proyecto en 2 minutos

**Mi Mascota** es una aplicación web para una **veterinaria**. Reemplaza la agenda de papel y las fichas físicas.

**Problema real:** las citas se anotan en papel y por teléfono (se duplican), los historiales de las mascotas se
pierden, nadie recuerda cuándo toca el refuerzo de una vacuna y el dueño no sabe cuánto ingresa.

**Qué hace el sistema:**

| Módulo | Para qué sirve |
|---|---|
| **Usuarios y roles** | Cada empleado entra con su cuenta y solo ve/hace lo que le corresponde. |
| **Clientes y mascotas** | Registro de dueños y de sus animales (una ficha por mascota). |
| **Servicios** | Catálogo con precio y duración (consulta, vacuna, baño…). |
| **Citas** | Agenda **sin choques de horario**; el sistema solo ofrece horas libres. |
| **Consultas (expediente)** | El veterinario registra síntomas, diagnóstico y tratamiento. |
| **Vacunas** | Registro con fecha del próximo refuerzo; avisa vencidas y próximas. |
| **Panel** | Citas del día, ingresos de 30 días y gráficas. |
| **API REST** | Servicios de datos en JSON que usa el frontend (y que podría usar una app móvil). |

**Los 3 roles:**

| Rol | Quién es | Puede |
|---|---|---|
| Administrador | Dueño | Todo (incluye usuarios y servicios) |
| Recepcionista | Atiende mostrador/teléfono | Clientes, mascotas, citas |
| Veterinario | Atiende pacientes | Ver su agenda, registrar consultas y vacunas |

**Frase para memorizar (elevator pitch):**
> *"Mi Mascota es un sistema web hecho con Django y PostgreSQL que digitaliza una veterinaria: registra clientes y
> mascotas, agenda citas sin traslapes, guarda el expediente clínico y avisa de refuerzos de vacunas. Tiene tres roles
> con permisos distintos, una API REST, pruebas automáticas, integración continua y está desplegado en Internet."*

---

## 2. Conceptos que necesitas dominar

Si algo de esta tabla no te suena, **detente aquí y estúdialo**: todo lo demás se apoya en esto.

### 2.1 Cliente-servidor y HTTP

```
 NAVEGADOR (cliente)                              SERVIDOR (Django)
 ┌────────────────┐   1. Petición HTTP            ┌─────────────────────┐
 │ Usuario hace   │  ───────────────────────────► │ Busca la vista que  │
 │ clic / escribe │   GET /clientes/?q=lopez      │ corresponde a la URL│
 │                │                               │ Consulta la BD      │
 │ Pinta la página│  ◄─────────────────────────── │ Genera HTML o JSON  │
 └────────────────┘   2. Respuesta (200 + HTML)   └─────────────────────┘
```

| Término | Significado | Ejemplo en el proyecto |
|---|---|---|
| **Petición (request)** | Lo que envía el navegador | `POST /clientes/nuevo/` con los datos del formulario |
| **Respuesta (response)** | Lo que devuelve el servidor | Una página HTML, un redirect o JSON |
| **GET** | Pedir/leer datos (no cambia nada) | Ver la lista de clientes |
| **POST** | Enviar datos para crear/cambiar algo | Guardar un cliente nuevo |
| **PUT / PATCH / DELETE** | Reemplazar / modificar parcial / borrar | Se usan en la API |
| **Códigos de estado** | 200 OK · 201 creado · 302 redirección · 400 datos inválidos · 403 prohibido · 404 no existe · 405 método no permitido · 409 conflicto · 500 error del servidor | `403` si un veterinario abre la página de usuarios |
| **Cookie / sesión** | El servidor te da un identificador que el navegador manda en cada petición para saber que ya iniciaste sesión | Al hacer login |

### 2.2 Patrón MVT (Modelo-Vista-Plantilla) de Django

Django es una variante de MVC. **Memoriza este cuadro:**

| Pieza | Qué hace | En el proyecto |
|---|---|---|
| **Modelo (Model)** | Describe los datos y las reglas; habla con la BD | `clientes/models.py`, `citas/models.py` |
| **Vista (View)** | Recibe la petición, usa modelos, decide qué responder | `clientes/views.py` |
| **Plantilla (Template)** | HTML con huecos que se llenan con datos | `clientes/templates/clientes/*.html` |
| **URLs** | Tabla que dice "esta dirección → esta vista" | `clientes/urls.py` |
| **Formulario (Form)** | Genera campos HTML y **valida** lo que escribe el usuario | `clientes/forms.py` |

> Ojo con el nombre: en Django la **"Vista"** es lo que en MVC clásico se llama **Controlador**, y la
> **"Plantilla"** es lo que se llama **Vista**. Es una pregunta típica.

### 2.3 Base de datos relacional y ORM

- **Relacional:** los datos están en **tablas** (filas y columnas) enlazadas por **claves** (PK = identificador de la
  fila, FK = referencia a la PK de otra tabla). Ej.: `mascota.cliente_id` apunta a `cliente.id`.
- **ORM (Object-Relational Mapper):** en vez de escribir SQL, escribes Python. Una **clase** = una tabla; un **atributo** = una columna; un **objeto** = una fila.

```python
# Python (ORM)                                        # SQL equivalente
Cliente.objects.filter(apellidos__icontains="lop")    # SELECT * FROM cliente WHERE apellidos ILIKE '%lop%'
Cliente.objects.create(nombres="Ana", ...)            # INSERT INTO cliente ...
```
- **Migraciones:** archivos que describen cambios en la estructura de la BD (crear tabla, añadir columna).
  `makemigrations` los genera a partir de los modelos y `migrate` los aplica.

### 2.4 Frontend vs. Backend

| | Frontend | Backend |
|---|---|---|
| Dónde corre | En el navegador | En el servidor |
| Qué hace | Muestra e interactúa | Lógica, seguridad, base de datos |
| Aquí | HTML, CSS (Bootstrap), JavaScript | Python / Django |

### 2.5 AJAX / Fetch y API REST

- **AJAX / `fetch`:** JavaScript pide datos al servidor **sin recargar la página** y actualiza solo una parte.
- **API REST:** un conjunto de direcciones (*endpoints*) que reciben y devuelven **JSON** (datos puros) en lugar de HTML.
  Cada URL representa un **recurso** (`/api/citas/`) y el verbo HTTP indica la acción (GET lee, POST crea, PATCH modifica, DELETE borra).

```json
{ "id": 1, "mascota_nombre": "Rocky", "estado": "PENDIENTE" }     ← esto es JSON
```

### 2.6 Seguridad web (lo básico)

| Ataque | Qué es | Defensa aquí |
|---|---|---|
| **SQL Injection** | Meter SQL malicioso en un campo | Usar el ORM (parametriza las consultas) |
| **XSS** | Meter `<script>` que se ejecuta en el navegador de otros | Django escapa el HTML automáticamente |
| **CSRF** | Otra web hace que tu navegador (con sesión abierta) envíe una acción a nuestro sitio | Token CSRF en cada formulario / `fetch` |
| **Contraseñas robadas** | Si roban la BD, ven las claves | Se guardan con **hash** (PBKDF2), nunca en texto |
| **Escalada de privilegios** | Un rol bajo hace acciones de uno alto | Se valida el rol **en el servidor** |

---

## 3. Tecnologías usadas y por qué

| Tecnología | Para qué | Por qué la elegimos |
|---|---|---|
| **Python 3.12 + Django 5.2** | Backend | Trae login, formularios, ORM, admin y seguridad integrados; el enunciado lo permite. |
| **Django REST Framework (DRF)** | API REST | Estándar de facto para APIs en Django: serializers, permisos, paginación. |
| **PostgreSQL** | BD en producción | Relacional, robusta, gratuita en Render. |
| **SQLite** | BD en tu PC | No requiere instalar nada; Django cambia de BD solo con `DATABASE_URL`. |
| **Bootstrap 5** | Estilos y diseño responsivo | Sistema de rejillas y componentes listos; permitido en el enunciado. |
| **JavaScript (fetch)** | Interactividad | Búsqueda en vivo, horarios, cambio de estado, gráficas. Sin framework extra. |
| **Chart.js** | Gráficas del panel | Pequeña y sencilla. |
| **WhiteNoise + Gunicorn** | Servir la app en producción | Gunicorn ejecuta Django; WhiteNoise sirve CSS/JS. |
| **GitHub Actions** | CI | Corre las pruebas en cada push. |
| **Render** | Hosting | Plan gratuito con PostgreSQL y despliegue desde GitHub. |

**¿Por qué no React?** El enunciado pide una interfaz profesional y responsiva y permite plantillas de Django.
Con plantillas + `fetch` entregamos la misma interactividad con menos piezas (un solo proyecto, un solo despliegue)
y el equipo puede explicar todo el código. Esa es una decisión técnica válida y defendible.

---

## 4. Mapa de carpetas y archivos

```
mi-mascota/
├── manage.py                 ← "control remoto" de Django: runserver, migrate, test, seed_demo…
├── requirements.txt          ← librerías Python (pip install -r requirements.txt)
├── .env.example              ← plantilla de variables de entorno (secretos fuera del código)
├── build.sh · render.yaml    ← despliegue en Render
├── Procfile · Dockerfile     ← despliegue alternativo (Railway / Docker)
├── .github/workflows/ci.yml  ← integración continua
│
├── config/                   ← CONFIGURACIÓN GENERAL
│   ├── settings.py           ← todo: apps, BD, seguridad, idioma, estáticos, DRF
│   └── urls.py               ← tabla principal de URLs (reparte a cada app)
│
├── accounts/                 ← USUARIOS Y PERMISOS
│   ├── models.py             ← Usuario (con campo "rol")
│   ├── permissions.py        ← RolRequeridoMixin (web) y RolPermiso (API)  ⭐
│   ├── forms.py · views.py · urls.py · admin.py
│   └── templates/accounts/   ← login, lista y formulario de usuarios
│
├── clientes/                 ← CLIENTES Y MASCOTAS
├── servicios/                ← CATÁLOGO DE SERVICIOS
├── citas/                    ← AGENDA
│   └── models.py             ← Cita + reglas de negocio + horarios_disponibles()  ⭐
├── expedientes/              ← CONSULTAS Y VACUNAS
├── api/                      ← API REST
│   ├── serializers.py        ← convierte modelos ⇄ JSON y valida
│   ├── views.py              ← ViewSets (CRUD) y vistas especiales
│   └── urls.py               ← rutas /api/…
│
├── core/                     ← PIEZAS COMPARTIDAS
│   ├── views.py              ← panel (dashboard) y páginas de error
│   ├── mixins.py             ← búsqueda parcial (AJAX) y borrado protegido
│   ├── forms.py              ← BootstrapFormMixin (estiliza todos los formularios)
│   ├── validators.py         ← validar teléfono
│   ├── estadisticas.py       ← consultas del panel y de /api/estadisticas/
│   ├── testing.py            ← utilidades para las pruebas
│   └── management/commands/  ← seed_demo (datos de ejemplo) y crear_admin
│
├── templates/                ← base.html (menú y layout), 403.html, 404.html
├── static/
│   ├── css/app.css           ← estilos propios
│   └── js/                   ← app.js, citas_lista.js, cita_form.js, dashboard.js
└── docs/                     ← documentación del proyecto
```

**Patrón repetido en cada app** (aprendes una, conoces todas):

```
models.py   → qué datos hay
forms.py    → cómo se capturan y validan
views.py    → qué se hace con cada petición
urls.py     → qué dirección lleva a qué vista
templates/  → cómo se ve
tests.py    → cómo se comprueba que funciona
admin.py    → cómo aparece en el panel /admin/ de Django
```

---

## 5. Qué pasa cuando haces clic: el viaje de una petición

### 5.1 Ejemplo A — Abrir la lista de clientes (`GET /clientes/`)

```
1. Navegador pide  GET /clientes/
2. config/urls.py    → path("clientes/", include("clientes.urls"))      (reparte a la app)
3. clientes/urls.py  → path("", ClienteListView.as_view())               (encuentra la vista)
4. RolRequeridoMixin → ¿hay sesión? ¿el rol está permitido?            (si no: login o 403)
5. ClienteListView.get_queryset() → filtra por ?q= y ?estado=, anota total de mascotas
6. ListView pagina (10 por página) y pasa los datos a la plantilla
7. clientes/cliente_lista.html + _cliente_tabla.html → HTML final
8. Respuesta 200 con el HTML → el navegador lo muestra
```

### 5.2 Ejemplo B — Agendar una cita (el flujo más completo)

| Paso | Qué ocurre | Archivo |
|---|---|---|
| 1 | La recepcionista abre **Citas → Agendar**: `GET /citas/nueva/` | `citas/urls.py` |
| 2 | `CitaCrearView` verifica que su rol sea Admin/Recepción (si no, 403) | `citas/views.py`, `accounts/permissions.py` |
| 3 | Se dibuja el formulario `CitaForm` con la plantilla genérica | `citas/forms.py`, `core/templates/core/formulario.html` |
| 4 | Al elegir **servicio + veterinario + fecha**, JavaScript hace `fetch` a `/api/horarios-disponibles/?…` | `static/js/cita_form.js` |
| 5 | `HorariosDisponiblesView` llama a `horarios_disponibles()`, que calcula las horas libres y las devuelve en JSON | `api/views.py`, `citas/models.py` |
| 6 | JavaScript llena el `<select>` de horas con la respuesta (sin recargar) | `cita_form.js` |
| 7 | Al **guardar**, `POST /citas/nueva/` | |
| 8 | `CitaForm.clean()` junta fecha + hora en un `fecha_hora` y verifica que sea futura | `citas/forms.py` |
| 9 | Django ejecuta `Cita.clean()`: horario laboral, domingo, **traslape** del veterinario y de la mascota | `citas/models.py` |
| 10 | Si hay error → se vuelve a mostrar el formulario con el mensaje. Si no → `form_valid` asigna `creado_por`, guarda y redirige al detalle | `citas/views.py` |
| 11 | `Cita.save()` copia la duración del servicio a la cita | `citas/models.py` |

**Por qué se valida dos veces (paso 5 y paso 9):** el `fetch` solo *ayuda* al usuario. Un usuario malicioso podría saltarse
el JavaScript y enviar el POST a mano. **La validación que cuenta es la del servidor.**

### 5.3 Ejemplo C — Confirmar una cita sin recargar

```
clic en ✔ → citas_lista.js  → App.apiFetch("POST /api/citas/15/cambiar-estado/", {estado:"CONFIRMADA"})
          → CitaViewSet.cambiar_estado() → cita.puede_pasar_a("CONFIRMADA")? → guarda
          → responde JSON → JS muestra un aviso (toast) y recarga SOLO la tabla (contenedor.recargar())
```

---

## 6. Base de datos y modelos

Diagrama completo: [`docs/03_DIAGRAMA_ER.md`](docs/03_DIAGRAMA_ER.md). Resumen:

```
Usuario ─┬──< Cita >── Mascota >── Cliente
         ├──< Consulta >── Mascota
         └──< Vacuna  >── Mascota          Cita >── Servicio       Cita ──o Consulta (0..1)
```

| Modelo | Campos importantes | Detalles que debes saber |
|---|---|---|
| **Usuario** | `username`, `password` (hash), `rol`, `telefono`, `is_active` | Extiende `AbstractUser`: Django ya trae login, hash y permisos. Solo añadimos `rol`. Configurado en `settings.AUTH_USER_MODEL`. |
| **Cliente** | `nombres`, `apellidos`, `telefono`, `email`, `nit`, `activo` | `telefono` usa un validador (8 dígitos). `nombre_completo` es una *property* (se calcula, no se guarda). |
| **Mascota** | `cliente` (FK), `nombre`, `especie`, `raza`, `sexo`, `fecha_nacimiento`, `notas`, `activo` | `edad` se calcula con la fecha de nacimiento. `especie` y `sexo` usan `TextChoices` (lista cerrada de opciones). |
| **Servicio** | `nombre` (único), `precio`, `duracion_minutos`, `activo` | La duración decide cuánto ocupa una cita en la agenda. |
| **Cita** | `mascota`, `veterinario`, `servicio`, `fecha_hora`, `duracion_minutos`, `estado`, `motivo`, `creado_por` | Contiene las reglas de negocio (sección 9). |
| **Consulta** | `mascota`, `cita` (1-1 opcional), `veterinario`, `fecha`, `peso_kg`, `temperatura_c`, `sintomas`, `diagnostico`, `tratamiento`, `costo` | Una consulta puede existir **sin cita** (urgencias). |
| **Vacuna** | `mascota`, `nombre`, `fecha_aplicacion`, `proxima_dosis`, `aplicada_por` | `vencida` es una property: `proxima_dosis < hoy`. |

### Decisiones de diseño que debes poder defender

1. **`on_delete=PROTECT`** en las relaciones clínicas: si intentas borrar un cliente con mascotas (o una mascota
   con historial), Django lanza `ProtectedError` y el sistema responde "no se puede eliminar, desactívalo".
   *Por qué:* en una clínica el historial es información valiosa y a veces legal; no debe perderse por un clic.
2. **Campo `activo` (borrado lógico):** para "quitar" algo sin destruirlo. Los usuarios no se borran, se desactivan.
3. **`Cita.duracion_minutos` se copia del servicio:** si mañana el servicio pasa de 30 a 60 min, las citas ya agendadas
   no se corren ni crean choques. Es una desnormalización **intencional**.
4. **Valores calculados no se guardan** (`edad`, `fin` de la cita, `nombre_completo`): se derivan, así no hay datos contradictorios (3FN).
5. **Índices** (`db_index` / `Meta.indexes`) en columnas que se buscan mucho: apellidos, fecha de cita, `(veterinario, fecha_hora)`, `proxima_dosis`.
6. **Dinero con `DecimalField`**, nunca `float` (los flotantes tienen errores de redondeo).

### Comandos de base de datos

```bash
python manage.py makemigrations   # genera archivos de migración a partir de los modelos
python manage.py migrate          # los aplica a la base de datos
python manage.py seed_demo        # carga datos de ejemplo (usuarios, clientes, citas…)
python manage.py shell            # consola Python con Django cargado (para probar el ORM)
```

---

## 7. Autenticación y autorización (roles)

- **Autenticación = "¿quién eres?"** → login con usuario y contraseña (`accounts/views.py`, `LoginView` de Django).
- **Autorización = "¿qué puedes hacer?"** → según el `rol` del usuario.

### 7.1 Cómo se implementó (archivo clave: `accounts/permissions.py`)

```python
ADMIN_RECEPCION = (Usuario.Rol.ADMIN, Usuario.Rol.RECEPCION)     # grupos de roles reutilizables

class RolRequeridoMixin(LoginRequiredMixin, UserPassesTestMixin):
    roles_permitidos = TODOS
    def test_func(self):                                         # ¿el rol del usuario está permitido?
        return tiene_rol(self.request.user, self.roles_permitidos)
    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            raise PermissionDenied                               # con sesión pero sin permiso → 403
        return super().handle_no_permission()                    # sin sesión → redirige al login
```

Cada vista solo declara qué roles admite:

```python
class ClienteCrearView(RolRequeridoMixin, SuccessMessageMixin, CreateView):
    roles_permitidos = ADMIN_RECEPCION        # ← el veterinario recibe 403
```

### 7.2 Dos capas de control (importante)

| Capa | Qué hace | Es segura? |
|---|---|---|
| **Interfaz** (`puede_gestionar`, `puede_atender` en `core/context_processors.py`) | Oculta botones que el rol no puede usar | ❌ Solo comodidad: se puede saltar |
| **Servidor** (`RolRequeridoMixin` / `RolPermiso`) | Rechaza la petición con 403 | ✅ Esta es la seguridad real |

### 7.3 En la API: `RolPermiso`

Cada ViewSet define `roles_lectura` y `roles_escritura`; `RolPermiso` decide según el método HTTP
(GET/HEAD/OPTIONS = lectura; el resto = escritura).

### 7.4 Contraseñas

Django guarda un **hash PBKDF2** (nunca el texto). Validadores en `settings.AUTH_PASSWORD_VALIDATORS`
(mínimo 8 caracteres, no muy común, no solo números, no parecida al usuario). El logout es por **POST** (Django 5) para evitar cierres de sesión forzados por enlaces maliciosos.

---

## 8. Formularios y validaciones

El enunciado pide **validaciones en cliente y servidor**.

| Dónde | Cómo | Ejemplo |
|---|---|---|
| **Cliente (navegador)** | Atributos HTML5 (`required`, `type="date"`, `min`, `max`, `step`) + clase `needs-validation` de Bootstrap con `app.js` que bloquea el envío si algo falta | Peso entre 0.01 y 500; fecha mínima = hoy |
| **Servidor (Django)** | Validadores de campo, `clean_<campo>()`, `clean()` del formulario y `clean()` del modelo | Teléfono con regex; fecha de nacimiento no futura; traslapes de citas |

**Regla de oro:** *el cliente mejora la experiencia, el servidor garantiza la verdad.*

### Capas de validación del servidor (de más simple a más compleja)

1. **Validador de campo** — `core/validators.py` (`RegexValidator` del teléfono), `MinValueValidator`, `MaxValueValidator` en modelos.
2. **`clean_<campo>()`** en el formulario — ej. `MascotaForm.clean_fecha_nacimiento` (no futura), `ClienteForm.clean_nombres` (normaliza a "Ana").
3. **`clean()` del formulario** — reglas que cruzan campos: `VacunaForm` (próxima dosis > aplicación), `CitaForm` (fecha + hora → futura).
4. **`clean()` del modelo** — reglas de negocio que también aplican en el admin y la API: `Cita.clean()`.

### `BootstrapFormMixin`
`core/forms.py` recorre los campos y les pone `form-control`, `form-select` o `form-check-input`. Así no repetimos clases en cada formulario.

### `core/formulario.html`
Una plantilla genérica dibuja **cualquier** formulario (campos, errores, ayuda, botones). Cada módulo la extiende y solo define el título y el botón Cancelar.

---

## 9. La parte estrella: reglas de la agenda de citas

Aquí está el valor real del sistema frente a "un CRUD sin contexto" (palabras del enunciado).
Archivo: **`citas/models.py`**. Estúdialo línea por línea.

### 9.1 Estados y transiciones

```
 PENDIENTE ──► CONFIRMADA ──► (consulta guardada) ──► ATENDIDA
     │             │
     ├─► CANCELADA └─► CANCELADA / NO_ASISTIO
```

```python
TRANSICIONES = {
    PENDIENTE:  (CONFIRMADA, CANCELADA),
    CONFIRMADA: (CANCELADA, NO_ASISTIO),
}
```
- "Atendida" **no** se puede poner a mano: ocurre automáticamente al guardar la consulta (así nunca hay una cita "atendida" sin consulta).
- Estados finales (atendida, cancelada, no asistió) no admiten más cambios.
- Solo `PENDIENTE` y `CONFIRMADA` **ocupan horario** (`ESTADOS_ACTIVOS`): una cita cancelada libera el espacio.

### 9.2 `Cita.clean()` — qué rechaza

| Regla | Mensaje |
|---|---|
| El usuario elegido debe tener rol veterinario | "El usuario seleccionado no es veterinario." |
| La cita debe caber en el horario laboral (por defecto 8:00-17:00) | "…dentro del horario de atención" |
| No se atiende los domingos | "La clínica no atiende los domingos." |
| **El veterinario no puede tener dos citas que se traspongan** | "El veterinario ya tiene una cita en ese horario." |
| **La mascota no puede estar en dos citas a la vez** | "Esta mascota ya tiene una cita en ese horario." |
| (En el formulario/API) La fecha debe ser futura | "La cita debe ser en una fecha y hora futuras." |

### 9.3 ¿Cómo se detecta un traslape?

Dos intervalos `[inicio, fin)` se traslapan **si y solo si**:
```
existente.inicio < nueva.fin   Y   existente.fin > nueva.inicio
```
En el código (`_hay_traslape`): se traen las citas activas cercanas del veterinario y se comprueba esa condición.
Por eso una cita 10:00-10:30 **sí** permite otra 10:30-11:00 (el fin es exclusivo) pero **no** una de 10:15.

### 9.4 `horarios_disponibles()` — cómo se calculan las horas libres

```
desde la apertura hasta (cierre − duración), cada 30 min:
    descartar si el inicio ya pasó
    descartar si choca con alguna cita activa del veterinario
    → lo demás son horas libres
```
Un servicio de 2 horas (esterilización) nunca ofrece el último bloque del día porque no cabría.
Este mismo cálculo lo usa el formulario (vía API) y está probado en `citas/tests.py`.

### 9.5 Otros detalles

- `Cita.save()` copia `duracion_minutos` desde el servicio (ver 6, decisión 3).
- En el formulario, `CitaForm._update_errors` mueve los errores de `fecha_hora` al campo `hora` (porque `fecha_hora` no es un campo visible del formulario; se arma con `fecha` + `hora`).
- Al **editar**, el horario de la propia cita cuenta como libre (parámetro `cita` / `excluir_cita_id`).
- Flujo "Atender": `ConsultaCrearView.form_valid` está en `@transaction.atomic`: **o se guardan ambas cosas** (consulta y cita "atendida") **o ninguna**. Es una pregunta frecuente ("¿qué pasa si falla a la mitad?").

### 9.6 Dos personas agendando al mismo tiempo (condición de carrera)

`clean()` valida **antes** de guardar. Si dos recepcionistas eligen el mismo veterinario y la misma hora casi al
mismo tiempo, las dos validaciones podrían pasar (ninguna ve todavía la cita de la otra) y se guardarían ambas.
Por eso `Cita.save()` **vuelve a revisar los traslapes dentro de una transacción con bloqueo de filas**:

```
transaction.atomic():
    SELECT ... FOR UPDATE  sobre el veterinario   ← la 2.ª petición se queda esperando aquí
    SELECT ... FOR UPDATE  sobre la mascota
    ¿hay traslape?  → ValidationError("El veterinario ya tiene una cita en ese horario.")
    INSERT de la cita
COMMIT  ← se libera el bloqueo; la 2.ª petición continúa, ve la cita nueva y es rechazada
```

- Siempre se bloquea primero el veterinario y luego la mascota (mismo orden) → no hay *deadlocks*.
- Un guardado parcial (`save(update_fields=["estado"])`, el cambio de estado) no mueve la cita en la agenda y no revisa.
- `GuardarCitaMixin` (formulario) y `CitaViewSet._guardar` (API) convierten ese error en un mensaje normal / 400, no en un 500.
- En SQLite `select_for_update()` no hace nada (SQLite escribe de una transacción a la vez); el bloqueo real es en PostgreSQL.
- Prueba: `CitaConcurrenciaTests` abre dos hilos y comprueba que la segunda reserva **espera** y luego es rechazada.
  Solo corre con PostgreSQL (en SQLite aparece como *skipped*); el CI la ejecuta.

---

## 10. Vistas y mixins

Usamos **vistas basadas en clases (CBV)** de Django: `ListView`, `DetailView`, `CreateView`, `UpdateView`, `DeleteView`.
Ya traen el 90 % del trabajo del CRUD; nosotros personalizamos lo necesario.

| Vista genérica | Hace | Ejemplo |
|---|---|---|
| `ListView` | Lista objetos, con paginación (`paginate_by = 10`) | `ClienteListView` |
| `DetailView` | Muestra uno | `MascotaDetalleView` |
| `CreateView` / `UpdateView` | Formulario para crear / editar y guardar | `ClienteCrearView` |
| `DeleteView` | Confirma y borra | `EliminarProtegidoView` |

**Mixins** = clases pequeñas que se "mezclan" para añadir comportamiento:

| Mixin | Archivo | Aporta |
|---|---|---|
| `RolRequeridoMixin` | `accounts/permissions.py` | Login + control de rol |
| `SuccessMessageMixin` | Django | Mensaje verde al guardar |
| `ParcialListMixin` | `core/mixins.py` | Si la URL trae `?parcial=1`, devuelve solo la tabla (para la búsqueda en vivo) y conserva los filtros al paginar |
| `EliminarProtegidoView` | `core/mixins.py` | Borrado que atrapa `ProtectedError` y explica por qué no se puede |

**Orden importa:** `class X(RolRequeridoMixin, ParcialListMixin, ListView)` — los mixins van a la izquierda, la vista genérica a la derecha.

**Dos técnicas importantes en las listas:**
- `select_related("cliente")` evita el problema **N+1** (una consulta SQL extra por cada fila).
- `get_queryset()` se sobreescribe para aplicar los filtros (`?q=`, `?estado=`, `?especie=`).

---

## 11. Plantillas y herencia

**Lenguaje de plantillas de Django (DTL):**

| Sintaxis | Uso | Ejemplo |
|---|---|---|
| `{{ variable }}` | Imprimir un valor (escapado automáticamente) | `{{ c.nombre_completo }}` |
| `{% if %} … {% endif %}` | Condición | `{% if puede_gestionar %}` |
| `{% for x in lista %} … {% empty %}` | Bucle (con caso vacío) | tablas |
| `{% url 'app:nombre' pk %}` | Genera una URL desde su nombre (si cambia la ruta, no se rompe) | `{% url 'citas:cita_detalle' c.pk %}` |
| `{{ valor\|filtro }}` | Transformar | `{{ fecha\|date:"d/m/Y" }}`, `{{ texto\|truncatechars:70 }}` |
| `{% csrf_token %}` | Token anti-CSRF (obligatorio en formularios POST) | todos los formularios |
| `{% extends %}` / `{% block %}` | **Herencia** | ver abajo |
| `{% include %}` | Insertar un fragmento | `_paginacion.html` |

**Herencia de plantillas:**

```
templates/base.html            ← menú lateral, barra superior, mensajes, scripts globales
   ├─ core/formulario.html     ← formulario genérico  ← cliente_form.html, mascota_form.html, cita_form.html…
   ├─ clientes/cliente_lista.html   (incluye _cliente_tabla.html y core/_paginacion.html)
   └─ core/dashboard.html …
```

- **Fragmentos `_tabla.html`:** son la parte de la lista que cambia. La página completa los incluye y, para la
  búsqueda en vivo, el servidor devuelve **solo** el fragmento. *Un único archivo sirve para ambos casos.*
- **`core/context_processors.py`:** variables disponibles en **todas** las plantillas (nombre del negocio, `puede_gestionar`, `puede_atender`).
- **Etiquetas propias:** `core/templatetags/ui.py` (`clase_estado` da el color del badge; `icono_especie`).

---

## 12. Frontend: Bootstrap y JavaScript (fetch)

### 12.1 Bootstrap y diseño responsivo

- **Rejilla de 12 columnas:** `class="col-12 col-md-6 col-lg-3"` = ancho completo en celular, mitad en tablet, un cuarto en escritorio.
- **Puntos de quiebre:** `sm` ≥576 · `md` ≥768 · `lg` ≥992 · `xl` ≥1200 px.
- `d-none d-md-table-cell` oculta una columna en celular (las tablas no se desbordan; además van dentro de `table-responsive`).
- **Menú lateral:** `offcanvas-lg` → fijo a la izquierda en pantallas grandes y deslizable con el botón ☰ en celular.
- `<meta name="viewport" …>` en `base.html` es lo que hace que el celular use su ancho real.
- Componentes usados: *cards, badges, alerts, toasts, dropdown, offcanvas, pagination, forms validation*.

### 12.2 `static/js/app.js` — el JavaScript común

| Función | Qué hace |
|---|---|
| `aviso(mensaje, tipo)` | Muestra un *toast* (aviso temporal). Usa `textContent` para evitar XSS. |
| `apiFetch(url, {method, body})` | Envuelve `fetch`: manda la cookie de sesión, añade el **token CSRF** en métodos que modifican datos, convierte el cuerpo a JSON y **lanza un error legible** si la respuesta no es 2xx. |
| `iniciarBusqueda(form)` | Búsqueda en vivo (ver abajo). |
| Validación | Los formularios `.needs-validation` bloquean el envío si no pasan `checkValidity()`. |

```js
async function apiFetch(url, { method = "GET", body = null } = {}) {
  const opciones = { method, credentials: "same-origin", headers: { Accept: "application/json" } };
  if (method !== "GET") opciones.headers["X-CSRFToken"] = csrf();          // protección CSRF
  if (body !== null) { opciones.headers["Content-Type"] = "application/json"; opciones.body = JSON.stringify(body); }
  const respuesta = await fetch(url, opciones);
  const datos = respuesta.status === 204 ? null : await respuesta.json().catch(() => null);
  if (!respuesta.ok) throw new Error(/* mensaje del servidor */);
  return datos;
}
```

### 12.3 Las 4 interacciones con fetch (¡estas se demuestran en la presentación!)

| # | Dónde | Archivo JS | Qué hace | Endpoint / URL |
|---|---|---|---|---|
| 1 | Listas (clientes, mascotas, citas, consultas, vacunas) | `app.js` | **Búsqueda en vivo**: al escribir (espera 300 ms) pide la misma URL con `?parcial=1`, reemplaza la tabla y actualiza la URL con `history.replaceState` | `GET /clientes/?q=…&parcial=1` (devuelve HTML parcial) |
| 2 | Formulario de cita | `cita_form.js` | Carga las **horas libres** al cambiar servicio/veterinario/fecha. Un contador (`ultimaPeticion`) evita que una respuesta lenta pise a una más nueva | `GET /api/horarios-disponibles/` (JSON) |
| 3 | Lista de citas | `citas_lista.js` | Botones **confirmar / cancelar / no asistió** sin recargar la página y luego recarga solo la tabla | `POST /api/citas/{id}/cambiar-estado/` |
| 4 | Panel | `dashboard.js` | Pide los datos y dibuja las **gráficas** con Chart.js | `GET /api/estadisticas/` |

**Truco para estudiar:** abre la app, pulsa **F12 → Network → Fetch/XHR** y repite cada acción: verás las peticiones reales, sus respuestas y códigos.

**Mejora progresiva:** si JavaScript fallara, los formularios de búsqueda siguen funcionando como formularios GET normales (la página completa se recarga). Las acciones que dependen de JS son las 4 de arriba.

---

## 13. La API REST

Documentación de endpoints: [`docs/08_API.md`](docs/08_API.md). Aquí, el **cómo funciona**.

```
Petición JSON ─► Router ─► ViewSet ─► Permiso (RolPermiso) ─► Serializer (valida) ─► Modelo ─► BD
                                                      respuesta JSON ◄─ Serializer (convierte) ◄──┘
```

| Concepto | Archivo | Qué es |
|---|---|---|
| **Serializer** | `api/serializers.py` | Convierte un objeto Python ⇄ JSON y **valida** los datos entrantes. `CitaSerializer.validate()` reutiliza `Cita.clean()` para aplicar las **mismas reglas** que el formulario web (no se duplica la lógica). |
| **ViewSet** | `api/views.py` | Una clase que da list/create/retrieve/update/destroy. `CitaViewSet` solo permite crear/leer/editar (sin borrar: una cita se cancela). |
| **Router** | `api/urls.py` | Genera las URLs de cada ViewSet automáticamente (`/api/clientes/`, `/api/clientes/{id}/`). |
| **@action** | `CitaViewSet.cambiar_estado` | Endpoint extra: `POST /api/citas/{id}/cambiar-estado/`. |
| **APIView** | `HorariosDisponiblesView`, `EstadisticasView` | Endpoints a medida que no son un CRUD. |
| **Paginación / búsqueda / orden** | `settings.REST_FRAMEWORK` | `?page=`, `?search=`, `?ordering=` listos para todos. |
| **Autenticación** | `settings.REST_FRAMEWORK` | Sesión (frontend) y **Token** (`POST /api/token/`) para otros clientes (Postman, app móvil). |

Detalles que muestran dominio:
- **409 Conflict** al borrar algo con relaciones (`ProtegidoDestroyMixin`).
- **`read_only_fields = ("estado",)`**: el estado no se puede cambiar editando la cita; solo con la acción controlada.
- `total_mascotas` viene de una **anotación** (`Count`) para evitar consultas por fila.

---

## 14. Seguridad

Resumen con **dónde está** cada defensa (todo se puede señalar en el código durante la presentación):

| Tema | Implementación | Archivo |
|---|---|---|
| Hash de contraseñas | PBKDF2 por defecto de Django + 4 validadores | `settings.py` |
| Control de acceso | Mixins por rol y `RolPermiso` | `accounts/permissions.py` |
| CSRF | Middleware + `{% csrf_token %}` + cabecera `X-CSRFToken` en `fetch` | `settings.py`, `app.js` |
| XSS | Autoescape de plantillas; `textContent` en JS | plantillas, `app.js` |
| SQL Injection | Solo ORM | todo el proyecto |
| Secretos | Variables de entorno; `SECRET_KEY` **obligatoria** en producción (si falta, la app no arranca) | `settings.py` |
| HTTPS | `SECURE_SSL_REDIRECT`, `SECURE_PROXY_SSL_HEADER`, HSTS, cookies `Secure` (solo si `DEBUG=False`) | `settings.py` |
| Clickjacking | `X_FRAME_OPTIONS = "DENY"` | `settings.py` |
| Sesión | Cookie `HttpOnly`, expira a las 8 h | `settings.py` |
| Integridad de datos | `PROTECT`, validaciones de servidor | modelos |
| Repositorio limpio | `.env` y `db.sqlite3` en `.gitignore` | `.gitignore` |

Revisión automática: `python manage.py check --deploy`.

---

## 15. Pruebas automáticas

**Qué es una prueba automática:** código que ejecuta funciones del sistema y comprueba (`assert`) que el resultado sea el esperado.
Sirven para detectar errores al cambiar código ("regresiones") y para demostrar que el sistema cumple las reglas.

```bash
python manage.py test                       # 67 pruebas
python manage.py test citas                 # solo la app citas
python manage.py test --verbosity 2         # muestra el nombre de cada una
```

- Cada prueba corre en una **base de datos temporal** (no toca tus datos).
- `core/testing.py` define `BaseTestCase`: crea un usuario por rol, un cliente, una mascota y un servicio.
- `self.client` simula un navegador (`self.client.post(url, datos)`); `force_login` inicia sesión sin pasar por el formulario.
- La API se prueba con `APIClient`.
- Patrón **AAA**: *Arrange* (preparar) → *Act* (actuar) → *Assert* (comprobar).

Qué cubren (por qué son valiosas): permisos por rol, validaciones, traslapes, horas libres, atención de citas, API (códigos 200/400/403/405/409),
búsqueda/paginación y borrado protegido. Detalle en [`docs/06_PLAN_DE_PRUEBAS.md`](docs/06_PLAN_DE_PRUEBAS.md).

---

## 16. Git, CI/CD y despliegue

| Concepto | En palabras simples | En el proyecto |
|---|---|---|
| **Git** | Historial de versiones del código | Commits con mensaje claro |
| **Rama** | Línea paralela de trabajo | `feature/HU-07-…` |
| **Pull Request** | "Quiero fusionar mi rama; revísenla" | Plantilla en `.github/pull_request_template.md` |
| **CI** (Integración Continua) | Un robot corre las pruebas en cada cambio | `.github/workflows/ci.yml` |
| **CD** (Entrega/Despliegue Continuo) | Cada cambio aprobado se publica solo | Render redespliega al hacer push a `main` |

**El ciclo completo:**
```
feature/rama ──► Pull Request ──► CI (pruebas en PostgreSQL) ──► revisión de un compañero
        ──► merge a develop/main ──► Render ejecuta build.sh (instala, collectstatic, migrate, crear_admin) ──► app actualizada
```

**Producción vs. desarrollo** (muy preguntado):

| | Desarrollo (tu PC) | Producción (Render) |
|---|---|---|
| `DJANGO_DEBUG` | True (muestra errores detallados) | **False** (nunca mostrar errores al público) |
| Base de datos | SQLite | PostgreSQL (`DATABASE_URL`) |
| Servidor | `runserver` | `gunicorn` |
| Archivos estáticos | los sirve runserver | `collectstatic` + WhiteNoise |
| HTTPS | no | sí (redirección + HSTS) |

Guías detalladas: [`docs/05_GIT_Y_COLABORACION.md`](docs/05_GIT_Y_COLABORACION.md) y [`docs/07_DESPLIEGUE.md`](docs/07_DESPLIEGUE.md).

---

## 17. Preguntas del docente (con respuestas)

### Sobre el negocio y la gestión
1. **¿Qué problema real resuelve su sistema?** — Citas en papel que se duplican, historiales extraviados, refuerzos de vacunas olvidados y falta de datos para decidir. (Sección 1 y `docs/01`.)
2. **¿Cómo supieron qué necesitaba el negocio?** — Levantamiento: visita/entrevista (`docs/01`), de ahí salieron el PRD y el backlog. *(Cuenten la entrevista real que hicieron.)*
3. **¿Qué quedó fuera de alcance y por qué?** — Facturación electrónica, inventario, portal para clientes, mensajería automática: para entregar algo completo y bien probado en el tiempo del curso. (`docs/02`, sección 6.)
4. **¿Cómo aplicaron Scrum?** — Roles (PO, SM, 3 devs), sprints de 1 semana, backlog priorizado, tablero con 5 columnas, daily, review y retrospectiva. (`docs/04`.)
5. **¿Cómo evitaron que una sola persona hiciera todo?** — Reparto de módulos, ramas por historia, Pull Requests obligatorios revisados por otro integrante, `main` protegida. Se ve en *Insights → Contributors*. (`docs/05`.)

### Sobre arquitectura y tecnología
6. **¿Por qué Django?** — Autenticación, ORM, formularios y protección CSRF/XSS integrados; arquitectura clara; el enunciado lo permite.
7. **¿Qué es MVT y cómo se relaciona con MVC?** — Modelo = datos; Vista (Django) = controlador; Plantilla = vista de MVC. (Sección 2.2.)
8. **¿Qué es una migración?** — Un archivo que registra un cambio de estructura de la BD; versiona el esquema y se aplica con `migrate`.
9. **¿Qué es el ORM y qué ventaja tiene?** — Escribir consultas con Python; evita SQL injection, es portable entre SQLite y PostgreSQL.
10. **¿Por qué SQLite en desarrollo y PostgreSQL en producción?** — SQLite no requiere instalación; PostgreSQL es robusto para producción. Django lo cambia con `DATABASE_URL` sin tocar el código. *Riesgo:* diferencias entre motores; por eso el CI corre las pruebas contra PostgreSQL.
11. **¿Por qué una API REST si ya tienen vistas con plantillas?** — Las interacciones dinámicas (horas libres, estados, gráficas) necesitan datos sin recargar; la API los entrega en JSON y deja la puerta abierta a una app móvil u otros sistemas.
12. **¿Qué diferencia hay entre `fetch` y un formulario normal?** — El formulario recarga toda la página; `fetch` pide datos en segundo plano y actualiza solo una parte.
13. **¿Por qué plantillas de Django y no React?** — Menos piezas, un solo despliegue, el equipo puede explicar todo el código y el enunciado lo permite. (Sección 3.)
14. **¿Qué es un serializer?** — Convierte objetos ⇄ JSON y valida entradas de la API.
15. **¿Qué es un mixin y para qué lo usaron?** — Clase pequeña que añade comportamiento por herencia múltiple: control de roles, búsqueda parcial, borrado protegido.

### Sobre reglas de negocio y datos
16. **¿Cómo evitan que dos citas se traslapen?** — `Cita.clean()` busca citas activas del veterinario cuyo intervalo choque (`inicio_existente < fin_nuevo` y `fin_existente > inicio_nuevo`). Se aplica en el formulario y en la API. (Sección 9.)
17. **¿Y si dos personas agendan exactamente al mismo tiempo?** — Es una *condición de carrera*: ambas validaciones podrían pasar antes de guardar. `Cita.save()` lo resuelve: bloquea la fila del veterinario y de la mascota con `select_for_update()` dentro de una transacción y vuelve a revisar los traslapes; la segunda petición espera y recibe el error (sección 9.6).
18. **¿Por qué guardan `duracion_minutos` en la cita si ya está en el servicio?** — Para que cambiar el servicio después no mueva ni cree choques en citas ya agendadas. Desnormalización intencional.
19. **¿Por qué `PROTECT` y no `CASCADE`?** — `CASCADE` borraría el historial clínico al borrar un cliente. `PROTECT` lo impide y el sistema ofrece desactivar.
20. **¿Por qué el estado "Atendida" no se puede poner a mano?** — Para garantizar consistencia: una cita atendida siempre tiene su consulta. Se marca dentro de una transacción al guardar la consulta.
21. **¿Qué es `@transaction.atomic`?** — Agrupa operaciones: todas se confirman o, si una falla, se deshacen todas.
22. **¿Qué está en tercera forma normal y qué no?** — Todo, salvo la copia deliberada de la duración. (`docs/03`.)

### Sobre seguridad
23. **¿Cómo protegen las contraseñas?** — Hash PBKDF2 con sal; nunca texto plano; validadores de complejidad.
24. **¿Qué es CSRF y cómo lo evitan?** — Un sitio malicioso hace que tu navegador envíe una acción a nuestro sitio. Se evita con un token secreto por sesión en cada formulario y en la cabecera `X-CSRFToken` de los `fetch`.
25. **¿Basta con ocultar los botones a quien no tiene permiso?** — No: el usuario podría escribir la URL. La verificación real está en el servidor (`RolRequeridoMixin`, `RolPermiso`) y está probada.
26. **¿Qué pasa si `DEBUG=True` en producción?** — Se muestran errores con código y configuración a cualquiera: grave. Por eso en producción es `False` y `SECRET_KEY` es obligatoria.

### Sobre calidad y despliegue
27. **¿Cómo prueban el sistema?** — 67 pruebas automáticas (permisos, validaciones, citas, API) + checklist manual; el CI las ejecuta en cada push/PR.
28. **¿Qué es CI/CD?** — CI: pruebas automáticas en cada cambio. CD: despliegue automático. Con GitHub Actions + Render.
29. **¿Cómo se despliega y de dónde salen los secretos?** — Render ejecuta `build.sh`; secretos en variables de entorno del panel de Render, no en el repositorio.
30. **¿Qué mejorarían?** — Ver sección 19.

---

## 18. Ejercicios prácticos

Hacerlos es la mejor forma de **demostrar dominio**: si puedes modificar el proyecto, lo entiendes.

### Ejercicio 1 — Agregar el campo "microchip" a la mascota
1. `clientes/models.py`: añade `microchip = models.CharField(max_length=20, blank=True)` a `Mascota`.
2. `python manage.py makemigrations` y `python manage.py migrate`.
3. `clientes/forms.py`: añade `"microchip"` a `fields` de `MascotaForm`.
4. `clientes/templates/clientes/mascota_detalle.html`: muestra `{{ object.microchip|default:"—" }}`.
5. `api/serializers.py`: añade `"microchip"` a `fields` de `MascotaSerializer`.
6. Escribe una prueba en `clientes/tests.py` y corre `python manage.py test`.

**Qué demuestra:** el recorrido completo modelo → migración → formulario → plantilla → API → prueba.

### Ejercicio 2 — Cambiar el horario de atención
En `.env` pon `HORARIO_APERTURA=9` y `HORARIO_CIERRE=18`, reinicia y mira que `/citas/nueva/` ofrezca horas de 9:00 a 17:30.
*Demuestra:* configuración por entorno.

### Ejercicio 3 — Nuevo estado "En consulta"
1. `Cita.Estado`: añade `EN_CONSULTA`.
2. `TRANSICIONES`: permite `CONFIRMADA → EN_CONSULTA`.
3. `ESTADOS_ACTIVOS`: inclúyelo (sigue ocupando horario).
4. `core/templatetags/ui.py`: asígnale color.
5. `makemigrations` / `migrate`. Prueba en `citas/tests.py`.

### Ejercicio 4 — Un nuevo filtro
Añade a la lista de mascotas el filtro "esterilizados": un `<select>` en `mascota_lista.html` y un `if` en `MascotaListView.get_queryset()`. La búsqueda en vivo ya lo soportará sola, porque `app.js` envía todos los campos del formulario.

### Ejercicio 5 — Un endpoint nuevo
Crea `GET /api/vacunas/proximas/` que devuelva los refuerzos de los próximos 30 días (usa `APIView` y `RolPermiso`, y pruébalo con Postman o `curl`).

### Ejercicio 6 — Romper y reparar (para entender el CI)
Quita a propósito la validación de traslape en `Cita.clean()`, corre `python manage.py test` y observa **qué pruebas fallan y por qué**. Luego revierte con Git (`git restore citas/models.py`).

---

## 19. Limitaciones y mejoras futuras

Reconocer límites **sube** la credibilidad. Estas son las reales:

| Limitación | Detalle | Mejora posible |
|---|---|---|
| Agenda protegida solo desde Django | El bloqueo de 9.6 está en `Cita.save()`; un `UPDATE`/`INSERT` hecho directo en la base (o `bulk_create`) no lo pasa | Restricción de exclusión de PostgreSQL (`ExclusionConstraint` + `btree_gist`) |
| Sin bloqueo por intentos fallidos de login | Un atacante podría probar contraseñas | `django-axes` o límite de peticiones |
| Sin recordatorios automáticos | Se listan los refuerzos, pero no se envía WhatsApp/correo | Tareas programadas (Celery / cron) + API de mensajería |
| Sin bitácora de auditoría | No se registra quién cambió qué | `django-simple-history` |
| Sin facturación ni inventario | Fuera de alcance acordado | Módulos futuros |
| Zona horaria única (Guatemala) | Suficiente para una sucursal | Configuración por sucursal |
| Plan gratuito de hosting se "duerme" | Primera carga lenta | Plan pago o servicio *keep-alive* |
| Sin pruebas de interfaz automatizadas | La UI se prueba manualmente (checklist) | Playwright / Selenium |

---

## 20. Glosario

| Término | Significado |
|---|---|
| **Endpoint** | Una URL de la API que hace algo concreto |
| **JSON** | Formato de texto para intercambiar datos (`{"clave": "valor"}`) |
| **CRUD** | Create, Read, Update, Delete: crear, leer, actualizar, borrar |
| **ORM** | Mapeo objeto-relacional: usar clases en lugar de SQL |
| **Migración** | Cambio versionado en la estructura de la BD |
| **Queryset** | Consulta del ORM (perezosa: se ejecuta al usarla) |
| **FK / PK** | Clave foránea / clave primaria |
| **CBV** | Class-Based View: vista basada en clase |
| **Mixin** | Clase que aporta una funcionalidad reutilizable por herencia |
| **Middleware** | Capa que procesa cada petición antes/después de la vista (sesión, CSRF…) |
| **Serializer** | Convierte modelos ⇄ JSON y valida |
| **CSRF / XSS / SQLi** | Tipos de ataque web (sección 2.6) |
| **Token** | Cadena secreta que identifica a un cliente de la API |
| **Estáticos** | Archivos CSS, JS e imágenes |
| **WSGI / Gunicorn** | Interfaz y servidor que ejecutan Django en producción |
| **Variable de entorno** | Configuración fuera del código (secretos, URLs) |
| **CI/CD** | Integración y despliegue continuos |
| **PR** | Pull Request: propuesta de fusionar una rama |
| **Sprint** | Periodo corto de trabajo en Scrum |
| **Backlog** | Lista priorizada de lo que falta por hacer |
| **DoD** | Definición de Terminado |
| **Responsivo** | La interfaz se adapta al tamaño de pantalla |
| **Borrado lógico** | Marcar como inactivo en vez de borrar |
| **N+1** | Error de rendimiento: una consulta extra por cada fila |
| **Idempotente** | Se puede ejecutar varias veces con el mismo resultado (como `crear_admin`) |

---

## 21. Autoevaluación

Responde **sin mirar**. Si fallas en más de 5, repasa la sección indicada.

1. Dibuja el flujo de una petición `GET /clientes/` desde el navegador hasta la respuesta. *(5)*
2. ¿Qué diferencia hay entre autenticación y autorización? ¿Dónde se implementa cada una? *(7)*
3. ¿Qué hace `makemigrations` y qué hace `migrate`? *(2.3)*
4. ¿Por qué se valida en cliente **y** en servidor? ¿Cuál es la que cuenta? *(8)*
5. Explica cuándo dos citas se traslapan y por qué 10:00-10:30 y 10:30-11:00 sí son compatibles. *(9.3)*
6. ¿Qué cuatro interacciones usan `fetch`? ¿Qué endpoint llama cada una? *(12.3)*
7. ¿Por qué `Cita.duracion_minutos` se copia del servicio? *(6)*
8. ¿Qué pasa si intentas borrar un cliente con mascotas? ¿Qué mecanismo lo logra? *(6, 10)*
9. ¿Cómo se protege el `fetch` contra CSRF? *(12.2, 14)*
10. ¿Qué cambia entre desarrollo y producción? *(16)*
11. ¿Por qué el veterinario recibe 403 al abrir `/clientes/nuevo/` aunque no vea el botón? *(7.2)*
12. ¿Qué es el problema N+1 y cómo se evita aquí? *(10)*
13. ¿Qué ventaja tiene que la API reutilice `Cita.clean()`? *(13)*
14. ¿Cómo comprueba el CI que no se rompió nada? *(15, 16)*
15. Menciona tres limitaciones reales del sistema y cómo las resolverías. *(19)*

> ✅ Cuando todos en el equipo puedan contestar esto **y** hayan completado los ejercicios 1-3, están listos para defender el proyecto.
