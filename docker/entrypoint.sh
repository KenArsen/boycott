#!/bin/sh

# Debug: Вывод информации о среде
echo "Starting entrypoint script with Poetry..."

# Применение миграций
echo "Applying database migrations..."
poetry run python manage.py migrate

## Сбор статических файлов
#echo "Collecting static files..."
#poetry run python manage.py collectstatic --no-input

# Запуск Gunicorn-сервера
echo "Starting Gunicorn server..."
exec poetry run gunicorn --bind :8000 config.wsgi:application
