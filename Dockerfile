# Используем базовый образ с Python
FROM python:3.11-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файлы проекта в контейнер
COPY ./photonumbergamebot ./photonumbergamebot
COPY poetry.lock pyproject.toml ./

# Устанавливаем Poetry
RUN pip install poetry

# Устанавливаем зависимости через Poetry
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

# Команда запуска
CMD ["python", "photonumbergamebot/__main__.py"]
