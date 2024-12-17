FROM python:3.13-slim

# Устанавливаем переменные окружения для Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Рабочая директория в контейнере
WORKDIR /app

# Скачиваем Poetry
RUN pip install poetry

# Копируем файлы проекта
COPY ../ /app/

# Устанавливаем зависимости с помощью Poetry
RUN poetry install --without dev --no-interaction --no-ansi

# Делаем скрипт entrypoint.sh исполнимым
RUN chmod +x /app/docker/entrypoint.sh

# Открываем порт 8000 для приложения
EXPOSE 8000

RUN poetry cache clear pypi --all --no-interaction \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/*

# Указываем команду для запуска контейнера
CMD ["/app/docker/entrypoint.sh"]
