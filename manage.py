#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

from config.settings.environment import env


def main():
    """Run administrative tasks."""
    # Получаем окружение (development или production) из .env
    environment = env.str("DJANGO_ENV", default="development")

    # Проверяем корректность значения окружения
    if environment not in ["development", "production"]:
        raise ValueError(
            f"Invalid DJANGO_ENV value: {environment}. Expected 'development' or 'production'."
        )

    # Устанавливаем настройки для Django в зависимости от окружения
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", f"config.settings.{environment}")

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
