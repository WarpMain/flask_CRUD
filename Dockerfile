# Этап 1: Сборка
FROM python:3.11-slim AS builder

# Устанавливаем переменную окружения для отключения буферизации в Python
ENV PYTHONUNBUFFERED 1

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файл requirements.txt в контейнер
COPY requirements.txt /app/

# Устанавливаем зависимости в текущем образе
RUN pip install --no-cache-dir -r requirements.txt

# Этап 2: Финальный образ
FROM python:3.11-slim

# Устанавливаем переменную окружения для отключения буферизации в Python
ENV PYTHONUNBUFFERED 1

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем установленные зависимости из первого этапа
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages

# Копируем только код приложения (без файлов зависимостей)
COPY . /app/

# Открываем порт, на котором будет работать Flask-приложение
EXPOSE 5000

# Команда для запуска Flask-приложения
CMD ["python", "app.py"]
