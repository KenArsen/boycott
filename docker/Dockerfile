FROM python:3.13-slim

# Устанавливаем переменные окружения для Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Рабочая директория в контейнере
WORKDIR /app

# Устанавливаем необходимые пакеты для Poetry
RUN apt-get update \
    && apt-get install -y curl \
    && curl -sSL https://install.python-poetry.org | python3 - \
    && apt-get clean

# Добавляем Poetry в PATH
ENV PATH="/root/.local/bin:$PATH"

# Копируем файлы проекта
COPY ../ /app/

# Копируем файлы проекта
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root --no-dev --no-interaction

# Делаем скрипт entrypoint.sh исполнимым
RUN chmod +x /app/docker/entrypoint.sh

# Открываем порт 8000 для приложения
EXPOSE 8000

RUN poetry cache clear pypi --all --no-interaction \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/*

# Указываем команду для запуска контейнера
CMD ["/app/docker/entrypoint.sh"]
