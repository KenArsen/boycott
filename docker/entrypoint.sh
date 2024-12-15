#!/bin/sh

set -e  # Прекратить выполнение при любой ошибке

# Debug: Вывод информации о среде
echo "Starting entrypoint script..."

# Debug: Убедиться, что зависимости установлены
echo "Checking installed dependencies..."
poetry show

# Применение миграций
echo "Applying database migrations..."
python manage.py migrate

# Сбор статических файлов
echo "Collecting static files..."
python manage.py collectstatic --no-input

# Запуск Gunicorn-сервера
echo "Starting Gunicorn server..."
exec gunicorn --bind :8000 config.wsgi:application
