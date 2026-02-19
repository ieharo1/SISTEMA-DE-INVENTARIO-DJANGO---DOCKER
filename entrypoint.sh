#!/bin/bash
set -e

# Root phase: prepare mounted volumes and drop privileges to non-root user.
if [ "$(id -u)" = "0" ]; then
  mkdir -p /app/staticfiles /app/media /app/logs
  chown -R app:app /app/staticfiles /app/media /app/logs /app
  exec gosu app "$0" "$@"
fi

echo "=== INVENTORY SYSTEM STARTUP ==="
echo "Waiting for PostgreSQL..."
while ! nc -z db 5432; do
  sleep 1
done
echo "PostgreSQL is ready"

echo "Creating cache table..."
python manage.py createcachetable || true

echo "Making migrations..."
python manage.py makemigrations --noinput || true

echo "Migrating database..."
python manage.py migrate --noinput

echo "Creating roles and seed data..."
python manage.py create_initial_data || true

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Creating superuser if not exists..."
python manage.py shell << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
username = "${DJANGO_SUPERUSER_USERNAME:-admin}"
email = "${DJANGO_SUPERUSER_EMAIL:-admin@inventory.com}"
password = "${DJANGO_SUPERUSER_PASSWORD:-admin123}"
if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print('Superuser created')
else:
    print('Superuser already exists')
EOF

echo "Starting Gunicorn..."
exec gunicorn inventory.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 4 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile - \
    --log-level info
