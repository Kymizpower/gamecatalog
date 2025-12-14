FROM python:3.13-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Копируем файл зависимостей
COPY requirements.txt .

# Устанавливаем Python зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . .

# Создаем директории для статических файлов и медиа
RUN mkdir -p /app/staticfiles /app/media

# Устанавливаем рабочую директорию в game_catalog
WORKDIR /app/game_catalog

# Собираем статические файлы
RUN python manage.py collectstatic --noinput || true

# Открываем порт
EXPOSE 8001

# Команда для запуска сервера
CMD ["python", "manage.py", "runserver", "0.0.0.0:8001"]

