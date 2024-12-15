import os

from django.core.wsgi import get_wsgi_application

from config.settings.environment import env

# Получаем окружение (development или production) из .env
environment = env.str("DJANGO_ENV", default="development")

# Проверяем корректность значения
if environment not in ["development", "production"]:
    raise ValueError(
        f"Invalid DJANGO_ENV value: {environment}. Expected 'development' or 'production'."
    )

# Устанавливаем настройки для Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", f"config.settings.{environment}")

# Инициализация WSGI-приложения
application = get_wsgi_application()
