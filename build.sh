#!/usr/bin/env bash
# Script de construcción para Render / Railway. Se ejecuta en cada despliegue.
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate --noinput
python manage.py crear_admin
# Si defines SEED_DEMO=true se cargan datos de ejemplo (solo para demostraciones).
if [ "${SEED_DEMO:-false}" = "true" ]; then
  python manage.py seed_demo
fi
