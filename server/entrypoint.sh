#!/usr/bin/env sh
set -e

# Default to production-ish behavior inside container
: "${DJANGO_DEBUG:=False}"
export DJANGO_DEBUG

python manage.py migrate --noinput

# collectstatic can fail if build artifacts are missing; keep container runnable
python manage.py collectstatic --noinput || true

exec gunicorn djangoproj.wsgi:application \
  --bind 0.0.0.0:${PORT:-8000} \
  --workers ${WEB_CONCURRENCY:-2} \
  --timeout ${GUNICORN_TIMEOUT:-120}
