# 5. Git y colaboración en equipo

El enunciado revisará: **participación de los integrantes, commits, ramas, Pull Requests, historial y organización
del repositorio**, y dice que debe evitarse que una sola persona haga casi todo. Esta guía explica cómo trabajar bien.

## 1. Crear el repositorio (lo hace una persona, una sola vez)

1. En GitHub: **New repository** → nombre `mi-mascota` → *Private* o *Public* → **sin** README (ya existe).
2. **Settings → Collaborators**: invitar a los otros 4 integrantes (y al docente si lo piden).
3. Desde la carpeta `mi-mascota/` del proyecto:

```bash
git init -b main
git add .
git commit -m "Proyecto base: Django, modelos, vistas, API y documentación"
git remote add origin https://github.com/USUARIO/mi-mascota.git
git push -u origin main
git switch -c develop
git push -u origin develop
```

> El `.gitignore` ya excluye `.venv/`, `.env` y `db.sqlite3`. **Nunca** subas contraseñas ni `.env`.

4. **Settings → Branches → Add rule** para `main`: *Require a pull request before merging* y
   *Require status checks (CI)*. Así nadie sube directo a `main` y todo pasa por revisión.

## 2. Estrategia de ramas (GitHub Flow simplificado)

```
main        ← siempre funcional y desplegable (lo que se presenta)
 └─ develop ← integración de lo que va terminado en el sprint
     ├─ feature/HU-07-agenda-citas
     ├─ feature/HU-14-vacunas
     ├─ fix/telefono-validacion
     └─ docs/prd
```

| Prefijo | Para qué |
|---|---|
| `feature/HU-XX-nombre-corto` | Una historia de usuario |
| `fix/descripcion` | Corregir un error |
| `docs/descripcion` | Documentación |
| `test/descripcion` | Pruebas |

## 3. Flujo diario de cada integrante

```bash
git clone https://github.com/USUARIO/mi-mascota.git     # solo la primera vez
cd mi-mascota
git switch develop && git pull                           # 1. partir de lo último
git switch -c feature/HU-14-vacunas                      # 2. rama propia
# ... programar ...
python manage.py test                                    # 3. correr pruebas ANTES de subir
git add -p                                               # 4. revisar qué se sube
git commit -m "Agrega filtro de refuerzos de vacunas"    # 5. commit pequeño y claro
git push -u origin feature/HU-14-vacunas                 # 6. subir la rama
```

7. En GitHub abrir un **Pull Request** hacia `develop` (la plantilla se rellena sola), enlazar la tarjeta/issue
   (`Closes #12`), pedir revisión a **otro** integrante.
8. El revisor comenta, pide cambios o aprueba. Al aprobar y pasar el CI → **Merge**.
9. Al cerrar el sprint, el Scrum Master abre un PR `develop → main`.

## 4. Mensajes de commit

Formato: **verbo en presente + qué cambia**, máximo ~70 caracteres.

✅ `Agrega validación de traslape en citas` · `Corrige cálculo de edad de mascotas` · `Documenta endpoints de la API`

❌ `cambios` · `fix` · `asdf` · `listo`

## 5. Cómo se verá el aporte de cada persona

El profesor puede ver en GitHub: **Insights → Contributors**, el historial de commits por autor, Pull Requests
abiertos/revisados y issues. Para que sea justo y real:

- Cada integrante configura su **propio nombre y correo** (los mismos de su cuenta GitHub):
  ```bash
  git config --global user.name  "Nombre Apellido"
  git config --global user.email "correo@ejemplo.com"
  ```
- **No** compartir una sola computadora/cuenta para todos los commits.
- Cada quien hace sus propios Pull Requests y **revisa al menos 2** de otros.
- Repartir módulos (ver `04_SCRUM.md` §6) y que cada persona aporte en todos los sprints, también en
  documentación y pruebas.

## 6. Resolver conflictos

```bash
git switch feature/mi-rama
git fetch origin
git merge origin/develop        # trae lo nuevo; si hay conflicto, Git marca los archivos
# abre los archivos, busca <<<<<<< ======= >>>>>>>, deja la versión correcta, guarda
git add archivo_resuelto.py
git commit                      # termina el merge
```

Para evitarlos: ramas cortas (1-3 días), `git pull` de `develop` a menudo y no reformatear archivos ajenos.

## 7. Integración continua (CI)

El archivo `.github/workflows/ci.yml` ejecuta automáticamente, en cada push y Pull Request:
verificación de configuración → verificación de migraciones → archivos estáticos → **todas las pruebas** contra
una base PostgreSQL temporal. Si algo falla, el PR muestra ❌ y no debe fusionarse.

## 8. Comandos de supervivencia

| Necesito… | Comando |
|---|---|
| Ver estado | `git status` |
| Ver historial bonito | `git log --oneline --graph --decorate -15` |
| Deshacer cambios no guardados de un archivo | `git restore archivo` |
| Quitar del área de preparación | `git restore --staged archivo` |
| Corregir el último mensaje (aún no subido) | `git commit --amend` |
| Guardar trabajo a medias | `git stash` / `git stash pop` |
| Ver quién cambió una línea | `git blame archivo` |
