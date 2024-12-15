import os

from django.core.asgi import get_asgi_application

from config.settings.environment import env

# Получаем среду окружения (development или production) из .env
environment = env.str("DJANGO_ENV", default="development")

# Проверяем, что значение корректное
if environment not in ["development", "production"]:
    raise ValueError(
        f"Неверное значение DJANGO_ENV: {environment}. Ожидается 'development' или 'production'."
    )

# Устанавливаем модуль настроек в зависимости от среды окружения
os.environ.setdefault("DJANGO_SETTINGS_MODULE", f"config.settings.{environment}")

# Инициализация ASGI-приложения
application = get_asgi_application()
