# 7. Despliegue en Internet (Render + PostgreSQL)

El enunciado exige que la aplicación esté **accesible en Internet**. Render ofrece plan gratuito para web
y PostgreSQL, y despliega directo desde GitHub. El archivo `render.yaml` ya describe todo.

> ⚠️ Cosas que deben saber del plan gratuito: la app "se duerme" tras ~15 min sin uso (la primera visita tarda
> ~1 minuto en despertar) y la base de datos gratuita expira a los ~30 días. **Abran la URL unos minutos antes de presentar.**
> Revisen los planes vigentes en render.com, pueden cambiar.

## Opción A — Blueprint (recomendada, 5 minutos)

1. Subir el proyecto a GitHub (ver `05_GIT_Y_COLABORACION.md`). El archivo `render.yaml` debe estar en la raíz del repo.
2. Entrar a <https://render.com> → iniciar sesión con GitHub.
3. **New + → Blueprint** → elegir el repositorio `mi-mascota` → *Apply*.
4. Render pide el valor de `DJANGO_ADMIN_PASSWORD` (es `sync: false`): escribir una contraseña **segura** para
   el usuario `admin`. No la pongan en el repositorio.
5. Esperar el build (ejecuta `build.sh`: instala dependencias, `collectstatic`, `migrate`, crea el admin y, con
   `SEED_DEMO=true`, carga los datos de ejemplo).
6. Abrir la URL `https://mi-mascota-xxxx.onrender.com` e iniciar sesión.

## Opción B — Manual

1. **New + → PostgreSQL** (plan Free). Copiar la *Internal Database URL*.
2. **New + → Web Service** → repositorio → Runtime *Python*.
   - Build Command: `./build.sh`
   - Start Command: `gunicorn config.wsgi:application`
3. Variables de entorno:

| Variable | Valor |
|---|---|
| `PYTHON_VERSION` | `3.12.8` |
| `DJANGO_DEBUG` | `False` |
| `DJANGO_SECRET_KEY` | cadena aleatoria larga (botón *Generate*) |
| `DATABASE_URL` | la *Internal Database URL* de la base de datos |
| `DJANGO_ADMIN_USER` | `admin` |
| `DJANGO_ADMIN_PASSWORD` | contraseña segura |
| `SEED_DEMO` | `true` (opcional, datos de ejemplo) |

Render define solo `RENDER_EXTERNAL_HOSTNAME`; `settings.py` lo agrega a `ALLOWED_HOSTS` y a los orígenes CSRF de confianza.

## Otras plataformas

| Plataforma | Qué usar |
|---|---|
| **Railway** | `Procfile` (incluido) + plugin PostgreSQL; definir las mismas variables. |
| **Docker / Azure / AWS** | `Dockerfile` (incluido); pasar las variables de entorno y `DATABASE_URL`. |
| **PythonAnywhere** | Crear web app Django manual + MySQL/Postgres; configurar WSGI apuntando a `config.wsgi`. |

## Problemas comunes

| Síntoma | Causa y solución |
|---|---|
| `DisallowedHost` | Falta el dominio en `DJANGO_ALLOWED_HOSTS` (en Render se agrega solo). |
| 403 CSRF al iniciar sesión | Definir `DJANGO_CSRF_TRUSTED_ORIGINS=https://tu-app.onrender.com`. |
| Sin estilos (CSS) | No corrió `collectstatic` (revisar `build.sh`) o falta WhiteNoise. |
| `RuntimeError: Define DJANGO_SECRET_KEY` | Falta la variable con `DJANGO_DEBUG=False`. |
| Error de conexión a la base | `DATABASE_URL` mal copiada; usar la URL *interna* de Render. |
| Redirecciones infinitas | Proxy sin cabecera HTTPS: dejar `DJANGO_SSL_REDIRECT=True` solo detrás de un proxy que envíe `X-Forwarded-Proto`. |

## Entrega continua (CD)

Con Render conectado a GitHub, **cada push a `main` dispara un nuevo despliegue automático**. Junto con el CI
(`.github/workflows/ci.yml`) se obtiene el ciclo: *Pull Request → pruebas automáticas → merge a `main` → despliegue*.
